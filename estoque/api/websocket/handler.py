from tornado.websocket import WebSocketHandler as TornadoWebSocketHandler

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
    connection = None

    def open(self) -> None:
        WebSocketHandler.connection = self
        logger.info("Cliente WebSocket conectado.")

    def on_message(self, message: str) -> None:
        dados = Mensagem.model_validate_json(message)

        if dados.acao == "finalizar":
            if dados.produtos:
                balancete_logger.info("========== BALANCETE ==========")
                for item in dados.produtos:
                    balancete_logger.info("Produto: %s | Código: %s | Quantidade: %s",
                        item.produto.nome,
                        item.produto.cod_barras,
                        item.quantidade,
                    )
                balancete_logger.info("===============================")

    def on_close(self) -> None:
        WebSocketHandler.connection = None
        logger.info("Cliente WebSocket desconectado.")