from pathlib import Path

from tornado.web import Application, StaticFileHandler

from estoque.api.websocket.connection_manager import ConnectionManager
from estoque.api.websocket.handler import WebSocketHandler
from estoque.api.http.index_handler import IndexHandler
from estoque.config import Settings

WEB_PATH = Path(__file__).resolve().parents[1] / "web"
STATIC_PATH = WEB_PATH / "static"

def make_app(
    connection_manager: ConnectionManager | None = None
) -> Application:
    manager = connection_manager or ConnectionManager()

    handlers = [
        (r"/", IndexHandler, {"web_path": WEB_PATH}),
        (r"/ws", WebSocketHandler, {"connection_manager": manager}),
        (r"/static/(.*)", StaticFileHandler, {"path": str(STATIC_PATH)}),
    ]

    return Application(
        handlers,
        static_path=str(STATIC_PATH),
        debug=False,
    )
