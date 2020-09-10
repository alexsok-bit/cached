# -*- encoding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Hashable
from numbers import Integral


class BaseCache(ABC):

    @abstractmethod
    def get(self, key: Hashable, version: Hashable = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: Hashable, value: Any, timeout: Integral = None, version: Hashable = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def has_key(self, key: Hashable, version: Hashable = None) -> bool:
        raise NotImplementedError
