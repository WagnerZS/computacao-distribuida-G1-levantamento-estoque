from tornado.websocket import WebSocketHandler as TornadoWebSocketHandler

from estoque.api.websocket.connection_manager import ConnectionManager
from estoque.api.websocket.entity import Mensagem

import logging

logger = logging.getLogger(__name__)

balancete_logger = logging.getLogger("balancete")
balancete_logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))

balancete_logger.addHandler(handler)
balancete_logger.propagate = False


class WebSocketHandler(TornadoWebSocketHandler):
    def initialize(self, connection_manager: ConnectionManager) -> None:
        self.connection_manager = connection_manager

    def open(self) -> None:
        self.connection_manager.add(self)
        logger.info("Cliente WebSocket conectado.")

    def on_message(self, message: str) -> None:
        dados = Mensagem.model_validate_json(message)

        if dados.acao == "produto_lido":
            self.connection_manager.broadcast_except(self, message)
        elif dados.acao == "enviar_levantamento":
            self.connection_manager.broadcast_except(self, message)
        elif dados.acao == "levantamento_completo":
            if dados.produtos:
                balancete_logger.info("========== BALANCETE ==========")
                for item in dados.produtos:
                    balancete_logger.info("Produto: %s | Código: %s | Quantidade: %s",
                        item.produto.nome,
                        item.produto.cod_barras,
                        item.quantidade,
                    )
                balancete_logger.info("===============================")
            else:
                balancete_logger.info("Balancete vazio!")
            self.connection_manager.broadcast(message)

    def on_close(self) -> None:
        self.connection_manager.remove(self)
        logger.info("Cliente WebSocket desconectado.")