from enum import StrEnum
from logging import basicConfig, ERROR, INFO, error, info, StreamHandler


class LoggerConstants(StrEnum):
    MEDIA_INVALID = "Media could not be validated for interaction."
    MEDIA_VALID = "Media is valid for interaction."

    MEDIA_COMMENT_FAIL = "Failed to comment on media."
    MEDIA_COMMENT_SUCCESS = "Successfully commented on media."

    MEDIA_LIKE_FAIL = "Failed to like media."
    MEDIA_LIKE_SUCCESS = "Successfully liked media."

    STORY_INVALID = "Story could not be validated for interaction."
    STORY_VALID = "Story is valid for interaction."

    STORY_LIKE_FAIL = "Failed to like story."
    STORY_LIKE_SUCCESS = "Successfully liked story."

    PERCENTAGE_OUT_OF_BOUNDS = "Percentage did not fall within set value."


class Logger:
    def __init__(self):
        basicConfig(format='[%(levelname)s]: %(message)s', level=INFO)

    def error(self, message: str):
        error(msg=message)

    def info(self, message: str):
        info(msg=message)
