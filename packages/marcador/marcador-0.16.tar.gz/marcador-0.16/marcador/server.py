import click
import json
import socket
import datetime

from marcador.lib import get_session, get_db_path, Bookmark, Core

def serialize(obj):
    if isinstance(obj, list):
        return [serialize(o) for o in obj]
    elif isinstance(obj, dict):
        return {k:serialize(v) for k,v in obj.items()}
    elif obj is None:
        return None
    else:
        return obj.serialize()


def run(core, cmd, args):
    f = getattr(core, cmd)
    return serialize(f(**args))


@click.command()
@click.option('--hostname', default='127.0.0.1')
@click.option('--port', type=int, default=6003)
def server(hostname, port):
    session = get_session(get_db_path())
    core = Core(session)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((hostname, port))

    while True:
        try:
            msg, addr = sock.recvfrom(1024)
            print(datetime.datetime.now(), addr, msg)
            msg = json.loads(msg)
            ret = run(core, msg['cmd'], msg['args'])
            sock.sendto(bytes(json.dumps(ret), 'utf-8'), addr)
        except Exception as e:
            print(datetime.datetime.now(), f"Error: {e}")
            continue

