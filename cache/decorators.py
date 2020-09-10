#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Created at 09.09.2020.
# Python 3.7.3 x64
# Contacts: alexandrsokolov@cock.li
#
import inspect
from functools import wraps
from numbers import Integral
from typing import Hashable, Text, Callable

from . import interface


def cached(cache_backend: interface.BaseCache, key: Hashable, timeout: Integral = None, version=None):

    if not isinstance(cache_backend, interface.BaseCache):
        raise TypeError(f"argument 'cache_backend' must be a BaseCache, not {type(cache_backend)}")

    if not isinstance(key, (Text, Callable)):
        raise TypeError(f"argument 'key' must be a Text or Callable, not {type(key)}")

    if timeout is not None and not isinstance(timeout, Integral):
        raise TypeError(f"argument 'timeout' must be a Integral, not {type(timeout)}")

    def wrapper(fun):

        @wraps(fun)
        def wrapped(*args, **kwargs):
            sig = inspect.signature(fun).bind(*args, **kwargs)
            sig.apply_defaults()
            sig = dict(sig.arguments)

            cache_key = key(sig) if callable(key) else sig.get(key, key)

            if cache_backend.has_key(cache_key, version=version):
                return cache_backend.get(cache_key, version=version)
            else:
                result = fun(*args, **kwargs)
                cache_backend.set(cache_key, result, timeout=timeout, version=version)
                return result

        return wrapped

    return wrapper
