import logging

from tornado.websocket import WebSocketHandler

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: set[WebSocketHandler] = set()

    def add(self, connection: WebSocketHandler) -> None:
        self._connections.add(connection)

    def remove(self, connection: WebSocketHandler) -> None:
        self._connections.discard(connection)

    def broadcast(self, mensagem: str) -> None:
        for connection in tuple(self._connections):
            try:
                connection.write_message(mensagem)
            except Exception as error:
                logger.error("Falha ao enviar mensagem pelo WebSocket: %s", error)
                self._connections.discard(connection)

    def broadcast_except(self, remetente: WebSocketHandler, mensagem: str) -> None:
        for connection in tuple(self._connections):
            if connection is remetente:
                continue

            try:
                connection.write_message(mensagem)
            except Exception as err:
                logger.error("Falha ao enviar mensagem pelo WebSocket: %s", err)
                self._connections.discard(connection)