import pyci
from pathlib import Path
from datetime import datetime
from subprocess import call

def on_success():
    with open("CI-results", "w") as f:
        f.write(f"success: {datetime.now()}")
    call(["git", "add", "CI-results"])
    call(["git", "commit", "-m", "pass"])
    call(["git", "push"])
def on_failure():
    with open("CI-results", "w") as f:
        f.write(f"failure: {datetime.now()}")
    call(["git", "add", "CI-results"])
    call(["git", "commit", "-m", "fail"])
    call(["git", "push"])


if __name__ == "__main__":
    print("now testing something else")
    try:
        call(["conda", "env", "update", "-f", "environment.yml"])
        print("do some testing")
        # raise ValueError("what happens on an error")
        on_success()
    except Exception as e:
        print(e)
        on_failure()    
