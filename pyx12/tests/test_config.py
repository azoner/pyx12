from __future__ import annotations
import os
import sys
import logging
import unittest
from typing import Any

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s %(levelname)s %(message)s',
                   stream=sys.stdout)

class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Setting up test case")

    def tearDown(self) -> None:
        self.logger.debug("Tearing down test case")
        super().tearDown()
        
    def assertIsInstance(self, obj: Any, cls: type | tuple[type, ...], msg: str | None = None) -> None:
        super().assertIsInstance(obj, cls, msg) 