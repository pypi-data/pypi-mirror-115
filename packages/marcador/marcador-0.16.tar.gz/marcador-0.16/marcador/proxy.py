from marcador.lib import  Bookmark, Tag, BookmarkTag, Core
import socket
import json
import datetime

def deserialize(obj):
    if isinstance(obj, list):
        return [deserialize(o) for o in obj]
    elif isinstance(obj, dict):
        if obj.get("type") is None:
            return {k:deserialize(v) for k,v in obj.items()}

        if obj["type"] == "bookmark":
            return Bookmark.deserialize(obj)
        elif obj["type"] == "tag":
            return Tag.deserialize(obj)
        elif obj["type"] == "bookmark_tag":
            return BookmarkTag.deserialize(obj)

    elif obj is None:
        return None
    elif isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return obj

class RemoteProxy():
    def __init__(self, addr):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def cmd(self, name, args):
        payload = bytes(json.dumps({'cmd': name, 'args': args}), 'utf-8')
        self.sock.sendto(payload, self.addr)
        msg, addr = self.sock.recvfrom(4096)
        return deserialize(json.loads(msg))

    def list(self):
        return self.cmd('list', {})

    def tags(self):
        return self.cmd('tags', {})

    def bookmark_tags(self, url):
        return self.cmd('bookmark_tags', {'url': url})

    def add(self, url):
        return self.cmd('add', {'url': url})

    def add_tag(self, url, tag):
        return self.cmd('add_tag', {'url': url, 'tag': tag})

    def delete(self, url):
        return self.cmd('delete', {'url': url})

    def open(self, url):
        return self.cmd('open', {'url': url})


class LocalProxy():
    def __init__(self, session):
        self.core = Core(session)

    def list(self):
        return self.core.list()

    def tags(self):
        return self.core.tags()

    def bookmark_tags(self, url):
        return self.core.bookmark_tags()

    def add(self, url):
        return self.core.add(url)

    def add_tag(self, url, tag):
        return self.core.add_tag(url, tag)

    def delete(self, url):
        return self.core.delete(url)

    def open(self, url):
        return self.core.open(url)
