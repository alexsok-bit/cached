#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Created at 09.09.2020.
# Python 3.7.3 x64
# Contacts: alexandrsokolov@cock.li
#
import functools
import unittest

from cache.decorators import cached
from cache.backend import MemoryCache


class CallCounter:
    call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return True


class TestLruCacheFormPython(unittest.TestCase):
    def setUp(self) -> None:
        self.counter = CallCounter()
        self.wrapped = functools.lru_cache()(self.counter)

    def test_call_once(self):
        for i in range(10):
            self.wrapped()
        self.assertEqual(self.wrapped.cache_info().misses, self.counter.call_count)

    def test_call_many(self):
        for i in range(1, 10):
            self.wrapped(i)
        self.assertEqual(self.wrapped.cache_info().misses, self.counter.call_count)

    def test_unhashable_args(self):
        param = {"key": "value"}
        with self.assertRaises(TypeError):
            self.wrapped(param)

    def test_args(self):
        for i in range(1, 10):
            self.wrapped(CallCounter())
        self.assertEqual(self.wrapped.cache_info().misses, self.counter.call_count)  # noqa

    def test_args_2(self):
        c = CallCounter()
        for i in range(1, 10):
            self.wrapped(c)
        self.assertEqual(self.wrapped.cache_info().misses, self.counter.call_count)


class TestCache(unittest.TestCase):
    def setUp(self) -> None:
        self.counter = CallCounter()
        self.wrapped = cached(MemoryCache(), key="default")(self.counter)

    def test_call_once(self):
        for i in range(10):
            self.wrapped()
        self.assertEqual(1, self.counter.call_count)

    def test_call_many(self):
        for i in range(1, 10):
            self.wrapped(i)
        self.assertEqual(1, self.counter.call_count)  # noqa

    def test_unhashable_args(self):
        param = {"key": "value"}
        # with self.assertRaises(TypeError):
        for i in range(1, 10):
            self.wrapped(param)
        self.assertEqual(1, self.counter.call_count)  # noqa

    def test_args(self):
        for i in range(1, 10):
            self.wrapped(CallCounter())
        self.assertEqual(1, self.counter.call_count)  # noqa

    def test_args_2(self):
        c = CallCounter()
        for i in range(1, 10):
            self.wrapped(c)
        self.assertEqual(1, self.counter.call_count)
