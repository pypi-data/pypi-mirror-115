import logging

from detect_and_display.utils.singleton import Singleton


class DetectAndDisplayLogger(metaclass=Singleton):
    """Logger of the module."""
    def __init__(self):
        self._logger = logging.getLogger('detect-and-display')
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(module)s%(funcName)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def get_logger(self):
        """Get logger"""
        return self._logger
