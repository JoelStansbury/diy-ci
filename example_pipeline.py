from datetime import datetime
from subprocess import call
import os

class Conda:
    """Maybe useful class"""
    EXE = os.environ["CONDA_EXE"]
    BAT = os.environ["CONDA_BAT"]
    ENV_PATH = "./.venv"
    ENV_FILE = "environment.yml"

    @classmethod
    def update(self):
        call([Conda.EXE, "env", "update", "-f", Conda.ENV_FILE, "-p", Conda.ENV_PATH])
        call([Conda.BAT, "deactivate"])
        call([Conda.BAT, "activate", Conda.ENV_PATH])

def respond(message):
    with open("CI-results", "w") as f:
        f.write(f"{message}: {datetime.now()}")
    call(["git", "add", "CI-results"])
    call(["git", "commit", "-m", message])
    call(["git", "push"])


if __name__ == "__main__":
    print("now testing something else")
    try:
        print("do something like this")
        # Conda.update()
        # check_call(["pip", "install", "-e", ".", "--no-deps"])
        # check_call(["pip", "check"])
        # check_call(["pytest"])
        raise ValueError("what happens on an error")
        respond("success")
    except Exception as e:
        print(e)
        respond("failure")
