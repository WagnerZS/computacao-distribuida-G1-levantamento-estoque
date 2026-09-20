import logging
import asyncio

from tornado.websocket import websocket_connect

from rich.console import Console

from estoque.domain.levantamento.service import LevantamentoService
from estoque.domain.produto.repository import ProdutoRepository
from estoque.api.websocket.entity import Mensagem
from estoque.config import Settings
from estoque.infra.input.serial.source import SerialInputSource

logger = logging.getLogger(__name__)

settings = Settings()

produtos = ProdutoRepository(settings.dir_dados).listar()
levantamento = LevantamentoService(produtos)

def enviar_levantamento(connection) -> None:
    mensagem = Mensagem(
        acao="finalizar",
        produtos=levantamento.obter_levantamento()
    )

    connection.write_message(mensagem.model_dump_json())

async def run() -> None:
    def on_leitura(produto_lido: bool) -> None:
        if produto_lido:
            produto = levantamento.registrar_leitura()

            logger.info("Produto lido: %s | Código: %s | Quantidade: %s", produto.nome, produto.cod_barras,
                next(
                    item.quantidade
                    for item in levantamento.obter_levantamento()
                    if item.produto.id == produto.id
                )
            )

    serial_source = SerialInputSource(settings=settings, on_update=on_leitura)
    connection = await websocket_connect("ws://localhost:8888/")

    await serial_source.start()

    logger.info("Conectado ao servidor WebSocket.")

    try:
        while True:
            message = await connection.read_message()

            if message is None:
                break

    except asyncio.CancelledError:
        enviar_levantamento(connection)
        raise


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        Console().print("Leitor encerrado", style="blue")


if __name__ == "__main__":
    main()