from subprocess import check_output, call

from .timed_cache import TimedCache

CACHE = TimedCache(default_timeout=10)

class Branch:

    def __init__(
        self,
        name,
        hash,
        commit_tag,
        is_head,
        is_active,
        is_ahead,
        is_behind,
        repo
    ):
        self.name=name
        self.hash=hash
        self.commit_tag=commit_tag
        self.is_head=is_head
        self.is_active = is_active
        self.is_ahead=is_ahead
        self.is_behind = is_behind
        self.repo=repo
    
    def checkout(self):
        self.repo._run(["git", "stash"])
        self.repo._run(["git", "checkout", self.name])
        self.repo._run(["git", "pull"])

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
        self._run(["git", "fetch"])

    @property
    def branches(self):
        self.fetch()

        # Info about local repo (must occur after `git fetch`)
        local_resp = self._fetch(["git", "branch", "-v"])
        lines = local_resp.split("\n")
        active = {}
        ahead = {}
        behind = {}
        for line in lines:
            if line.strip():
                is_active = False
                parts = line.split()
                if parts[0] == "*":
                    is_active = True
                    parts = parts[1:]
                name, hash, *info = parts

                ahead[name] = info[0] == "[ahead"
                behind[name] = info[0] == "[behind"
                active[name] = is_active

        # Info about remote repo
        remote_resp = self._fetch(["git", "branch", "-r", "-v"])

        branches = []
        lines = remote_resp.split("\n")
        head_name = lines[0].split("->")[1].strip()
        for line in lines[1:-1]:
            name, hash, *info = line.split()
            name = name[len("origin/"):]
            branches.append(
                Branch(
                    name=name,
                    hash=hash,
                    commit_tag=" ".join(info),
                    is_head=name==head_name,
                    is_active=active.get(name, False),
                    is_ahead=ahead.get(name, False),
                    is_behind=behind.get(name, True),
                    repo=self
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
        