# Trains and Updates Ultralytics HUB Models

from .auth import Auth
from .trainer import Trainer
from .yolov5_utils.general import LOGGER, PREFIX
from .yolov5_wrapper import clone_yolo

AUTH = Auth()
CONNECTED = False


def train_model(api_key='', model_id='') -> None:
    """Starts training from next in queue"""
    try:
        clone_yolo()
        # connect_to_hub(api_key=api_key)  # deprecated
        AUTH.api_key = api_key
        trainer = Trainer(model_id=model_id, auth=AUTH)  # No model so next in train queue is fetched
        if trainer.model is not None:
            trainer.start()
    except Exception as e:
        LOGGER.info(f"{PREFIX}{e}")


def connect_to_hub(api_key='', verbose=False) -> bool:
    """Authenticates user with Ultralytics HUB"""
    global CONNECTED

    if CONNECTED and verbose:
        print(f'{PREFIX}Already logged in.')
    elif not CONNECTED:
        CONNECTED = AUTH.attempt_api_key(api_key=api_key)

    return CONNECTED
