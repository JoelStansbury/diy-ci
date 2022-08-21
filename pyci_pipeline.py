import pyci
from pathlib import Path
from datetime import datetime
from subprocess import call, check_call
import sys
import os

CONDA = os.environ["CONDA_EXE"]
CONDA_BAT = os.environ["CONDA_BAT"]
PYTHON = sys.executable

def upload_results():
    call(["git", "filter-branch", "--tree-filter", "'rm -f CI-results'", "HEAD"])
    call(["git", "push", "origin", "--force", "--all"])

def on_success():
    call(["git", "rm", "CI-results"])
    with open("CI-results", "w") as f:
        f.write(f"success: {datetime.now()}")
    call(["git", "add", "CI-results"])
    call(["git", "commit", "-m", "pass"])
def on_failure():
    call(["git", "rm", "CI-results"])
    with open("CI-results", "w") as f:
        f.write(f"failure: {datetime.now()}")
    call(["git", "add", "CI-results"])
    call(["git", "commit", "-m", "fail"])


if __name__ == "__main__":
    print("now testing something else")
    try:
        call([CONDA, "env", "update", "-f", "environment.yml"])
        call([CONDA_BAT, "deactivate"])
        call([CONDA_BAT, "activate", "./.venv"])
        check_call(["pip", "install", "-e", ".", "--no-deps"])
        check_call(["pip", "check"])
        print("do some testing")
        # raise ValueError("what happens on an error")
        on_success()
    except Exception as e:
        print(e)
        on_failure()
