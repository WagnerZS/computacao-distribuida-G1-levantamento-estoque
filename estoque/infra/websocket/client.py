import asyncio
import logging

from tornado.websocket import websocket_connect

from estoque.config import Settings

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._connection = None

    @property
    def connection(self):
        return self._connection

    async def conectar(self):
        while True:
            try:
                self._connection = await websocket_connect("ws://localhost:8888/ws")
                logger.info("Conectado ao servidor WebSocket.")
                return self._connection
            except Exception as erro:
                logger.error("Não foi possível conectar ao servidor: %s", erro)
                await asyncio.sleep(self._settings.serial_reconnect_delay_seconds)

    async def reconectar(self):
        await asyncio.sleep(self._settings.serial_reconnect_delay_seconds)
        return await self.conectar()