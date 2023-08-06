import json
import subprocess
import json
import re

json_support = subprocess.run(
    ['ip', '-j', 'link'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


class Link():
    __slots__ = [
        'ifname',
        '_cache'
    ]

    def __init__(self, ifname: str, type: str = None, _create=True):
        self.ifname = ifname
        if not _create:
            self._refresh()

    @classmethod
    def load(cls, ifname: str):
        return cls(ifname, _create=False)

    def _refresh(self):
        if json_support:
            res = subprocess.run(['ip', '-j', 'link', 'show', 'dev', self.ifname],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            self._cache = json.loads(res.stdout)[0]
        else:
            res = subprocess.run(['ip', 'link', 'show', 'dev', self.ifname],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            p = re.compile(r'(?P<ifindex>\d+):\s+(?P<ifname>[\w-]{1,16}):\s+<(?P<flags>[\w,-]+)>\s+')
            self._cache = p.search(res.stdout).groupdict()

    @property
    def ifindex(self):
        return self._cache['ifindex']

    @property
    def flags(self):
        if isinstance(self._cache['flags'], str):
            return self._cache['flags'].split(',')
        return self._cache['flags']
