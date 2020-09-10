#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Created at 09.09.2020.
# Python 3.7.3 x64
# Contacts: alexandrsokolov@cock.li
#
import logging
import inspect

import raven

from cache.decorators import cached
from cache.backend import MemoryCache

logger = logging.getLogger('celery.tasks')


@cached(MemoryCache(), key="host")
def send_log(message=None, task_id=None, host=None, level=logging.INFO, job_name=None, index=None, object_id=None):
    sentry_dsn = "settings.SENTRY_DSN"
    previous_frame = inspect.currentframe().f_back
    filename, line_number, function_name, *_ = inspect.getframeinfo(previous_frame)

    if isinstance(message, Exception):
        message = f"{host}: {type(message).__name__}::{message.args}"

    logger.log(level,
               f"{filename} at line {line_number} in {function_name}\n"
               f"[host:{host}] [object_id:{object_id}] [task_id:{task_id}] [job_name:{job_name}] "
               f"[index:{index}]\n{message}")
    if level >= logging.ERROR and sentry_dsn != "not set":
        sentry_logger = raven.Client(sentry_dsn)
        sentry_log_id = sentry_logger.captureException(
            tags={"task_id": task_id, "host": host, "job_name": job_name, "index": index, "object_id": object_id})
        logger.log(level, f"Sentry id: {sentry_log_id}")
    return True


send_log()
