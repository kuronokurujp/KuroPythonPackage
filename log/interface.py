#!/usr/bin/env python
from abc import ABC, abstractmethod


# Loggerのインターフェイス
class ILoegger(ABC):
    """
    ロガーのインターフェイス.

    Release Notes:
        - 1.0.0 (2024-10-10): 新規作成.

    @version: 1.0.0
    """

    @abstractmethod
    def info(self, msg: str):
        raise NotImplementedError()

    @abstractmethod
    def warn(self, msg: str):
        raise NotImplementedError()

    @abstractmethod
    def err(self, msg: str):
        raise NotImplementedError()

    # ログファイルの整理
    @abstractmethod
    def clearnup(self):
        raise NotImplementedError()
