import json
import signal
import sys
from pathlib import Path
from time import time, sleep

import requests

from . import __version__
from .config import HUB_API_ROOT
from .yolov5_utils.general import LOGGER, PREFIX, emojis, threaded
from .yolov5_utils.hub_utils import check_dataset_disk_space, smart_request
from .yolov5_wrapper import YOLOv5Wrapper as YOLOv5

IS_COLAB = 'google.colab' in sys.modules
AGENT_NAME = f'python-{__version__}-colab' if IS_COLAB else f'python-{__version__}-local'
hub_logger = None


def signal_handler(signum, frame):
    """ Confirm exit """
    global hub_logger
    print(f'Signal received. {signum} {frame}')
    if isinstance(hub_logger, HUBLogger):
        hub_logger.alive = False
        del hub_logger
    sys.exit(signum)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


class Trainer:
    # HUB Trainer class

    def __init__(self, model_id, auth):
        self.auth = auth
        self.model = self._get_model(model_id)
        if self.model is not None:
            self._connect_callbacks()

    def _get_model_by_id(self):
        # return a specific model
        return

    def _get_next_model(self):
        # return next model in queue
        return

    def _get_model(self, model_id):
        # Returns model from database by id
        api_url = f"{HUB_API_ROOT}/models/{model_id}"
        headers = self.auth.get_auth_header()

        try:
            r = smart_request(api_url, method="get", headers=headers, thread=False, code=0)
            data = r.json().get("data", None)
            if not data: return
            assert data['data'], 'ERROR: Dataset may still be processing. Please wait a minute and try again.'  # RF fix
            self.model_id = data["id"]
            return data
        except requests.exceptions.ConnectionError as e:
            raise Exception('ERROR: The HUB server is not online. Please try again later.') from e

    def _connect_callbacks(self):
        global hub_logger
        callback_handler = YOLOv5.new_callback_handler()
        hub_logger = HUBLogger(self.model_id, self.auth)
        callback_handler.register_action("on_pretrain_routine_start", "HUB", hub_logger.on_pretrain_routine_start)
        callback_handler.register_action("on_pretrain_routine_end", "HUB", hub_logger.on_pretrain_routine_end)
        callback_handler.register_action("on_fit_epoch_end", "HUB", hub_logger.on_fit_epoch_end)
        callback_handler.register_action("on_model_save", "HUB", hub_logger.on_model_save)
        callback_handler.register_action("on_train_end", "HUB", hub_logger.on_train_end)
        self.callbacks = callback_handler

    def start(self):
        # Checks
        if not check_dataset_disk_space(self.model['data']):
            return

        # Train
        YOLOv5.train(self.callbacks, **self.model)


class HUBLogger:
    # Log YOLOv5 trainings to HUB

    def __init__(self, model_id, auth):
        self.agent_id = None  # identifies which instance is communicating with server
        self.model_id = model_id
        self.api_url = f'{HUB_API_ROOT}/models/{model_id}'
        self.auth_header = auth.get_auth_header()
        self.rate_limits = {'metrics': 3.0, 'ckpt': 900.0, 'heartbeat': 300.0}  # rate limits (seconds)
        self.t = {}  # rate limit timers (seconds)
        self.metrics_queue = {}  # metrics queue
        self.keys = [
            'train/box_loss',
            'train/obj_loss',
            'train/cls_loss',  # train loss
            'metrics/precision',
            'metrics/recall',
            'metrics/mAP_0.5',
            'metrics/mAP_0.5:0.95',  # metrics
            'val/box_loss',
            'val/obj_loss',
            'val/cls_loss',  # val loss
            'x/lr0',
            'x/lr1',
            'x/lr2']  # metrics keys
        self.alive = True  # for heartbeats
        self._heartbeats()  # start heartbeats

    def __del__(self):
        # Class destructor
        self.alive = False

    def on_pretrain_routine_start(self, *args, **kwargs):
        # YOLOv5 pretrained routine start
        pass

    def on_pretrain_routine_end(self, *args, **kwargs):
        # Start timer for upload rate limit
        LOGGER.info(emojis(f"{PREFIX}View model at https://hub.ultralytics.com/models/{self.model_id} 🚀"))
        self.t = {'metrics': time(), 'ckpt': time()}  # start timer on self.rate_limit

    def on_fit_epoch_end(self, *args, **kwargs):
        # Upload metrics after val end
        vals, epoch = args[:2]
        self.metrics_queue[epoch] = json.dumps({k: round(float(v), 5) for k, v in zip(self.keys, vals)})  # json string
        if time() - self.t['metrics'] > self.rate_limits['metrics']:
            self._upload_metrics()
            self.t['metrics'] = time()  # reset timer
            self.metrics_queue = {}  # reset queue

    def on_model_save(self, *args, **kwargs):
        # Upload checkpoints with rate limiting
        last, epoch, final_epoch, best_fitness, fi = args[:5]
        is_best = best_fitness == fi
        if time() - self.t['ckpt'] > self.rate_limits['ckpt']:
            LOGGER.info(f"{PREFIX}Uploading checkpoint {self.model_id}")
            self._upload_model(epoch, last, is_best)
            self.t['ckpt'] = time()  # reset timer

    def on_train_end(self, *args, **kwargs):
        # Upload final model and metrics with exponential standoff
        last, best, epoch, results = args[:4]
        LOGGER.info(emojis(f"{PREFIX}Training completed successfully ✅"))
        LOGGER.info(f"{PREFIX}Uploading final {self.model_id}")
        self._upload_model(epoch, best, map=results[3], final=True)  # results[3] is mAP0.5:0.95
        self.alive = False  # stop heartbeats
        LOGGER.info(emojis(f"{PREFIX}View model at https://hub.ultralytics.com/models/{self.model_id} 🚀"))

    # Internal functions ---
    def _upload_metrics(self):
        payload = {"metrics": self.metrics_queue.copy(), "type": "metrics"}
        smart_request(f'{self.api_url}', json=payload, headers=self.auth_header, code=2)

    def _upload_model(self, epoch, weights, is_best=False, map=0.0, final=False):
        # Upload a model to HUB
        file = None
        if Path(weights).is_file():
            with open(weights, "rb") as f:
                file = f.read()
        if final:
            smart_request(f'{self.api_url}/upload',
                          data={"epoch": epoch, "type": "final", "map": map},
                          files={"best.pt": file},
                          headers=self.auth_header,
                          retry=10,
                          timeout=3600,
                          code=4)
        else:
            smart_request(f'{self.api_url}/upload',
                          data={"epoch": epoch, "type": "epoch", "isBest": bool(is_best)},
                          headers=self.auth_header,
                          files={"last.pt": file},
                          code=3)

    @threaded
    def _heartbeats(self):
        while self.alive:
            r = smart_request(f'{HUB_API_ROOT}/agent/heartbeat/models/{self.model_id}',
                              json={"agent": AGENT_NAME, "agentId": self.agent_id},
                              headers=self.auth_header,
                              retry=0,
                              code=5,
                              thread=False)
            self.agent_id = r.json().get('data', {}).get('agentId', None)
            sleep(self.rate_limits['heartbeat'])
