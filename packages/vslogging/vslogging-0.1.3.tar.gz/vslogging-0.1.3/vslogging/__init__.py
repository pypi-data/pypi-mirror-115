# -*- coding: utf-8 -*-

__author__ = "Jason Smith"
__credits__ = ["Jason Smith"]
__email__ = "jasons2@cisco.com"

"""
Setup Logging for both console and file.
Default File name is 'Log_[basefilename].log'
Default Level is Debug
"""

import logging
import os

levels = {"debug" : logging.DEBUG,
            "info" : logging.INFO,
            "warning" : logging.WARNING,
            "error" : logging.ERROR,
            "critical" : logging.CRITICAL}

class vslogging:
    def __init__(self, fname="someLog", level="debug"):
        self.logger = logging.getLogger(fname)
        self.logger.setLevel(levels[level])
        self.ch = logging.StreamHandler()
        self.ch.setLevel(levels[level])
        self.fh = logging.FileHandler(fname + '.log')
        self.fh.setLevel(levels[level])

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def critical(self, msg: str) -> None:
        self.logger.error(msg)
    
def main():
    cl = customCiscoLogging()
    cl.info("some info")
    cl.debug("some debug")
    cl.warning("some warning")
    cl.critical("some critical")

if __name__ == '__main__':
    main()
