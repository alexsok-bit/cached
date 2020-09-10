#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Created at 10.09.2020.
# Python 3.7.3 x64
# Contacts: alexandrsokolov@cock.li
#
import functools
import inspect

counter = [0]


def foo(fun):

    def wrapper(*args, **kwargs):
        bounded_sig = inspect.signature(fun).bind(*args, **kwargs)
        bounded_sig.apply_defaults()
        print(dict(bounded_sig.arguments))
        return

    return wrapper


@foo
def wrapped(a, b, c, d):
    pass


wrapped("passed_a", "b", "c", d="passed_d")


@functools.lru_cache()
def bar(arg):
    counter[0] += 1
    return arg


for _ in range(2):
    try:
        raise Exception("Hello")
    except Exception as e:
        print(hash(e), id(e))
        bar(e)

print(bar.cache_info())
assert counter[0] == 1, counter
