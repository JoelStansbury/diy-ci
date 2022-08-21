from subprocess import check_output, call

from .timed_cache import TimedCache

CACHE = TimedCache(default_timeout=10)

class Branch:

    def __init__(self, name, hash, commit_tag, is_head):
        self.name=name
        self.hash=hash
        self.commit_tag=commit_tag
        self.is_head=is_head
    
    def checkout(self):
        call["git", "checkout", self.name]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Git:

    @CACHE
    def _fetch(self, args):
        print("FETCH:", " ".join(args))
        return check_output(args).decode()

    def _run(self, args):
        print("RUN:", " ".join(args))
        call(args)

    def stash(self):
        self._run(["git", "stash"])

    def fetch(self):
        self._run(["git", "fetch"])
    
    def checkout(self, branch):
        self._run(["git", "checkout", branch])
    
    @property
    def branches(self):
        self.fetch()
        resp = self._fetch(["git", "branch", "-r", "-v"])
        branches = []
        lines = resp.split("\n")
        head_name = lines[0].split("->")[1].strip()
        for line in lines[1:-1]:
            name, hash, *info = line.split()
            branches.append(
                Branch(
                    name=name,
                    hash=hash,
                    commit_tag=" ".join(info),
                    is_head=name==head_name
                )
            )
        return branches

    # @property
    # def pull_requests(self):
    #     resp = self._fetch(["git", "ls-remote", "origin"])
    #     for line in resp.split("\n"):
    #         if "refs/pull/" in line:
    #             source_hash = line.split()[0]
    #             dest_name = line.split("refs/pull/")[1]
    #             source = [b for b in self.branches if b.hash == source_hash][0]
    #             source = [b for b in self.branches if b.hash == source_hash][0]
        