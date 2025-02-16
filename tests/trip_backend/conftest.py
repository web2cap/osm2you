import os
import subprocess
import sys

PROJECT_DIR_NAME = "trip_backend"
os.environ["MODE"] = "TEST"

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(ROOT_DIR)

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
TESTS_PATH = os.path.join(ROOT_DIR, PROJECT_DIR_NAME)
sys.path.append(MANAGE_PATH)

pytest_plugins = [
    "fixtures.fixture_database",
    "fixtures.fixture_client",
    "fixtures.fixture_trip",
]

if PROJECT_DIR_NAME not in os.listdir(BASE_DIR) or not os.path.isdir(
    os.path.join(BASE_DIR, PROJECT_DIR_NAME)
):
    raise AssertionError(
        f"In `{BASE_DIR}` project folder not found `{PROJECT_DIR_NAME}`. "
        f"Make sure you have the correct project structure."
    )


print("\nRunning Ruff checks...")
try:
    result = subprocess.run(
        ["ruff", "check", MANAGE_PATH, TESTS_PATH, "--exclude", ".venv"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise AssertionError("Ruff formatting check failed. Fix the issues and try again.")
except FileNotFoundError as exc:
    raise AssertionError("Ruff is not installed.") from exc


def pytest_addoption(parser):
    parser.addoption(
        "--reuse-db",
        action="store_true",
        default=False,
        help="Reuse the existing database without recreating.",
    )
