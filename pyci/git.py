from subprocess import check_output, call

from .timed_cache import TimedCache

CACHE = TimedCache(default_timeout=10)

class Git:

    @property
    def pull_requests(self):
        resp = self._fetch(["git", "ls-remote", "origin"])
        return resp



    @CACHE
    def _fetch(self, args):
        return check_output(args).decode()

    def _run(self, args):
        print("COMMAND: ", " ".join(args))
        call(args)

    def stash(self):
        self._run(["git", "stash"])

    def fetch(self):
        self._run(["git", "fetch"])
    
    def checkout(self, branch):
        self._run(["git", "checkout", branch])
    
    @property
    def branches(self):
        resp = self._fetch(["git", "ls-remote", "origin"])
        return [
            x.split("refs/heads/")[1] 
            for x in resp.split("\n")
            if "refs/heads/" in x
        ]