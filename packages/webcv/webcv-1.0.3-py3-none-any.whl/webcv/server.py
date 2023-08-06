from pathlib import Path
import asyncio
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
import time
import json
import select
import traceback
import socket
from multiprocessing import Process, Pipe



def log_important_msg(msg, *, padding=3):
    msg_len = len(msg)
    width = msg_len + padding * 2 + 2
    print('#' * width)
    print('#' + ' ' * (width - 2) + '#')
    print('#' + ' ' * padding + msg + ' ' * padding + '#')
    print('#' + ' ' * (width - 2) + '#')
    print('#' * width)


def hint_url(url, port):
    log_important_msg(
        'The server is running at: {}'.format(url))


def _set_server_quart(conn, name, port):
    from quart import Quart, websocket, render_template

    app = Quart("webcv", template_folder=Path(__file__).parent.joinpath("templates").absolute().as_posix())

    package = None
    package_alive = False

    @app.route("/")
    async def index():
        return await render_template("index.html")

    @app.websocket("/stream")
    async def ws():
        should_send = True
        while True:
            global package
            global package_alive
            if conn.poll():
                package = conn.recv()
                package_alive = True
                should_send = True
            if not should_send:
                if conn.fileno() == -1:
                    break
                time.sleep(1)
                continue
            should_send = False

            try:
                if package is None:
                    await websocket.send(None)
                else:
                    delay, info_lst = package
                    await websocket.send(json.dumps((time.time(), package_alive, delay, info_lst)))
                    if package_alive:
                        message = await websocket.receive()
                        if message is None:
                            break
                        try:
                            if isinstance(message, bytes):
                                message = message.decode('utf8')
                            message = int(message)
                        except:
                            traceback.print_exc()
                            message = -1
                        conn.send(message)
                        package_alive = False
            except asyncio.CancelledError:
                break

    package = None
    package_alive = False
    hint_url('http://{}:{}'.format(socket.getfqdn(), port), port)
    app.run("0.0.0.0", port=port)


def get_server(name='webcv', port=7788):
    conn_server, conn_factory = Pipe()
    p_server = Process(
        target=_set_server_quart,
        args=(conn_server,),
        kwargs=dict(
            name=name, port=port,
        ),
    )
    p_server.daemon = True
    p_server.start()
    return p_server, conn_factory
