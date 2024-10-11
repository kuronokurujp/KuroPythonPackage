#!/usr/bin/env python
from ..loader import file
import pathlib


def test_loader_ini_file():
    try:
        ini_file: file.IniFile = file.IniFile(
            logic_filepath=pathlib.Path(__file__).parent / "data/loader/files/test.ini"
        )
        section = ini_file.section(name="acount")
        print("username: " + str(section["username"]))
        print("password" + str(section["password"]))

    except Exception as ex:
        print(ex)
        assert False
