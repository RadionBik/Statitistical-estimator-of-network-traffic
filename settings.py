import os
import logging
import sys
import pathlib


BASE_DIR = pathlib.Path(os.path.dirname(__file__))

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

