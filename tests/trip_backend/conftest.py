import os
import sys
from os.path import abspath, dirname

PROJECT_DIR_NAME = "trip_backend"
os.environ["MODE"] = "TEST"


root_dir = dirname(dirname(abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir_content = os.listdir(BASE_DIR)

if PROJECT_DIR_NAME not in root_dir_content or not os.path.isdir(
    os.path.join(BASE_DIR, PROJECT_DIR_NAME)
):
    assert False, (
        f"In `{BASE_DIR}` project folder not found `{PROJECT_DIR_NAME}`. "
        f"Make sure you have the correct project structure."
    )

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
sys.path.append(MANAGE_PATH)
