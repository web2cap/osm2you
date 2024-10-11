import os
import sys
from os.path import abspath, dirname

PROJECT_DIR_NAME = "trip_backend"


root_dir = dirname(dirname(abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
sys.path.append(MANAGE_PATH)

os.environ["MODE"] = "TEST"
