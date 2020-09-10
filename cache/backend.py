#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Created at 09.09.2020.
# Python 3.7.3 x64
# Contacts: alexandrsokolov@cock.li
#
from typing import Any, Hashable

from . import interface


class MemoryCache(interface.BaseCache):
    __slots__ = '_cache'

    def __init__(self):
        self._cache = {}

    def get(self, key: Hashable, **kwargs):
        return self._cache[key]

    def has_key(self, key: Hashable, **kwargs):
        return key in self._cache

    def set(self, key: Hashable, value: Any, **kwargs):
        self._cache[key] = value
