#!/usr/bin/env python
from ..log import logger
from pathlib import Path


def test_log_print():
    app_logger: logger.ILoegger = logger.AppLogger(
        log_dirpath=Path(__file__).parent / "data/log",
    )
    app_logger.info("info test")


def test_log_cleanup():
    app_logger: logger.ILoegger = logger.AppLogger(
        log_dirpath=Path(__file__).parent / "data/log", log_file_max=3
    )
    app_logger.clearnup()
    app_logger.info("info test")
