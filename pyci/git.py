from subprocess import check_output, call

from .timed_cache import TimedCache

CACHE = TimedCache(default_timeout=10)


class Branch:
    def __init__(self, name, hash, is_behind, repo):
        self.name = name
        self.hash = hash
        self.is_behind = is_behind
        self.repo = repo

    def checkout(self):
        self.repo._run(["git", "stash"])
        self.repo._run(["git", "checkout", self.name])
        self.repo._run(["git", "pull"])
        self.is_behind = False

    def __enter__(self):
        self.exit_branch = check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).strip()
        self.checkout()
    
    def __exit__(self):
        self.repo._run(["git", "checkout", self.exit_branch])
        self.repo._run(["git", "stash", "apply"])

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

    def fetch(self):
        self._run(["git", "fetch", "-p"])

    @property
    @CACHE(10)
    def branches(self):
        self.fetch()
        refs = [
            x.split() for x in self._fetch(["git", "for-each-ref"]).split("\n")[:-1]
        ]
        remote = {}
        local = {}
        for hash, _, url in refs:
            name = url.split("/")[-1]
            if "refs/remotes/origin" in url:
                remote[name] = hash
            elif "refs/heads/" in url:
                local[name] = hash
        del remote["HEAD"]
        branches = []
        for name, hash in remote.items():
            behind = local.get(name, None) != hash
            branches.append(Branch(name, hash, behind, self))
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
