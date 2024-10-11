#!/usr/bin/env python
import configparser
import pathlib


class IniFile(object):
    """
    Iniファイルをロードしてファイルのパラメータを取得.

    Release Notes:
        - 1.0.0 (2024-10-10): 新規作成.

    @version: 1.0.0
    """

    # ConfigParserオブジェクトを作成
    __config = configparser.ConfigParser()
    __path: pathlib.Path = None

    def section(self, name: str) -> configparser.ConfigParser:
        return self.__config[name]

    def __init__(self, logic_filepath: pathlib.Path) -> None:
        # INIファイルを読み込む
        # UTF-8エンコーディングでファイルを読み込む
        with open(logic_filepath, "r", encoding="utf-8") as configfile:
            self.__config.read_file(configfile)

    # エラーの場合はメッセージを返す
    def err_msg(self) -> str:
        if self.__path is None:
            return "Iniファイルのパスが存在しない"
        if self.__path.exists() is False:
            return f"{self.__path.as_posix()}にIniファイルのパスが存在しない"

        return None
