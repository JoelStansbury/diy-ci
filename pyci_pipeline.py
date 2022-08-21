import pyci
from pathlib import Path
from datetime import datetime

def on_success():
    with open("CI-results", "w") as f:
        f.write(f"success: {datetime()}")
def on_failure():
    with open("CI-results", "w") as f:
        f.write(f"failure: {datetime()}")


if __name__ == "__main__":
    print("now testing something else")
    try:
        print("do some testing")
        # raise ValueError("what happens on an error")
    except:
        print("I expected that error")
        on_failure()
    on_success()
    
    
