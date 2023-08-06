import inspect
import logging

from django.conf import settings


def log(message, level=logging.INFO):
    logger = logging.getLogger("application")
    logger.log(level, message)


def trace(message, level=logging.DEBUG, depth=0):
    frames = inspect.stack()

    current_frame = frames[1]

    message = '({0}:{1}:{2}): {3}'.format(
        current_frame[1].replace(settings.DJANGO_ROOT_PATH, ''),
        current_frame[3],
        current_frame[2],
        message,
    )

    if depth > 0:
        for i in range(2, min(depth+2, len(frames))):
            frame = frames[i]
            message += '\n\t{0}, line {1}, in {2}'.format(
                frame[1].replace(settings.DJANGO_ROOT_PATH, ''),
                frame[2],
                frame[3]
            )

    log(message, level)
