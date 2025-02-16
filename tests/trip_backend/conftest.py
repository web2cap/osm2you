import os
import sys
import subprocess
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
TESTS_PATH = os.path.join(root_dir, PROJECT_DIR_NAME)
sys.path.append(MANAGE_PATH)

pytest_plugins = [
    "fixtures.fixture_database",
    "fixtures.fixture_client",
    "fixtures.fixture_trip",
]


print("\nRunning Ruff checks...")
try:
    result = subprocess.run(
        ["ruff", "check", MANAGE_PATH, TESTS_PATH, "--exclude", ".venv"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        assert False, "Ruff formatting check failed. Fix the issues and try again."
except FileNotFoundError:
    assert False, "Ruff is not installed."



def pytest_addoption(parser):
    parser.addoption(
        "--reuse-db",
        action="store_true",
        default=False,
        help="Reuse the existing database without recreating.",
    )


