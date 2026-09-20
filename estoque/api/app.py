from pathlib import Path

from tornado.web import Application

from estoque.api.websocket.handler import WebSocketHandler

def make_app() -> Application:
    handlers = [
        (r"/", WebSocketHandler),
    ]
    return Application(
        handlers,
        debug=False,
    )
