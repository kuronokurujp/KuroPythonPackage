#!/usr/bin/env python
import logging
import datetime
from pathlib import Path
from logging import getLogger, config

# 同ディレクトリ内にあるロガーのインターフェイス
from .interface import ILoegger


class CustomDictConfigurator(config.DictConfigurator):
    """
    ロガーのカスタムハンドラー設定クラス.

    Release Notes:
        - 1.0.0 (2024-10-11): 新規作成.

    @version: 1.0.0
    """

    def resolve(self, s):
        class_def = None
        if s == "logger.PrintHandler":
            # 新しいモジュールパスやクラスを指定
            class_def = PrintHandler
        else:
            class_def = super().resolve(s)

        return class_def


class PrintHandler(logging.Handler):
    """
    printでログ出力するカスタムハンドラー.

    Release Notes:
        - 1.0.0 (2024-10-10): 新規作成.

    @version: 1.0.0
    """

    def flush(self):
        self.acquire()
        try:
            pass
        finally:
            self.release()

    def emit(self, record):
        try:
            msg = self.format(record)
            print(msg)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

    def __repr__(self):
        level = logging.getLevelName(self.level)
        name = "print"
        name = str(name)
        if name:
            name += " "
        return "<%s %s(%s)>" % (self.__class__.__name__, name, level)


class AppLogger(ILoegger):
    """
    アプリのログを取るロガー.

    Release Notes:
        - 1.0.0 (2024-10-10): 新規作成.
        - 1.0.1 (2024-10-11): 別プロジェクトで利用するログが生成しない問題を修正.

    @version: 1.0.1
    """

    __logger: logging.Logger = None
    __log_file_max: int = 2

    # 最初は外部ファイルにしようと思ったが, 改ざんされる可能性があるのでやめた
    __config_dict: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s"
            }
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "fileHandler": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "to be replaced",
                "encoding": "utf-8",
            },
            "printHandler": {
                "class": "logger.PrintHandler",
                "level": "INFO",
                "formatter": "simple",
            },
        },
        "loggers": {
            "app_logger": {
                "level": "DEBUG",
                "handlers": ["fileHandler", "printHandler"],
                "propagate": False,
            }
        },
        "root": {"level": "INFO"},
    }

    def __init__(self, log_dirpath: Path, log_file_max: int = 2) -> None:
        # logファイルを置くディレクトリを作成
        self.__log_dirpath = log_dirpath
        self.__log_dirpath.mkdir(parents=True, exist_ok=True)
        self.__log_file_max = log_file_max

        log_conf: dict = self.__config_dict

        # ファイル名をタイムスタンプで作成
        log_conf["handlers"]["fileHandler"]["filename"] = self.__log_dirpath.joinpath(
            "{}.logs".format(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        )

        config.dictConfigClass = CustomDictConfigurator
        config.dictConfig(log_conf)

        self.__logger = getLogger("app_logger")

    def info(self, msg: str):
        self.__logger.info(msg)

    def warn(self, msg: str):
        self.__logger.warning(msg)

    def err(self, msg: str):
        self.__logger.error(msg)

    # ログファイルの整理
    def clearnup(self):
        find_list: list = list(self.__log_dirpath.glob("*.logs"))
        if len(find_list) <= self.__log_file_max:
            return

        # 日付が古いファイルを優先して削除
        for i in range(0, self.__log_file_max, 1):
            del_filepath: Path = Path(find_list[i])
            del_filepath.unlink(missing_ok=True)


class PrintLogger(ILoegger):
    """
    アプリのログを取るロガー.

    Release Notes:
        - 1.0.0 (2024-10-10): 新規作成.

    @version: 1.0.0
    """

    def __init__(self) -> None:
        pass

    def info(self, msg: str):
        print("info: {}".format(msg))

    def warn(self, msg: str):
        print("warn: {}".format(msg))

    def err(self, msg: str):
        print("err: {}".format(msg))

    # ログファイルの整理
    def clearnup(self):
        pass
