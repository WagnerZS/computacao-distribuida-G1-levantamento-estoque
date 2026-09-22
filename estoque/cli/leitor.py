import logging
import asyncio

from estoque.domain.levantamento.service import LevantamentoService
from estoque.domain.produto.repository import ProdutoRepository
from estoque.api.websocket.entity import Mensagem
from estoque.config import Settings
from estoque.infra.input.serial.source import SerialInputSource
from estoque.api.websocket.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

settings = Settings()

produtos = ProdutoRepository(settings.dir_dados).listar()
levantamento = LevantamentoService(produtos)

async def conectar_servidor():
    while True:
        try:
            connection = await websocket_connect("ws://localhost:8888/")
            logger.info("Conectado ao servidor WebSocket.")
            return connection
        except OSError as erro:
            logger.error("Não foi possível conectar ao servidor: %s", erro)
            await asyncio.sleep(settings.serial_reconnect_delay_seconds)

def enviar_levantamento(connection) -> None:
    mensagem = Mensagem(
        acao="enviar_levantamento",
        produtos=levantamento.obter_levantamento()
    )

    connection.write_message(mensagem.model_dump_json())

async def ler_acao(connection_manager) -> None:
    while True:
        acao = await asyncio.to_thread(input, "> ")

        if acao.strip().lower() == "enviar":
            enviar_levantamento(connection_manager.connection)

async def receber_mensagens(connection_manager, connection) -> None:
    while True:
        mensagem = await connection.read_message()

        if mensagem is None:
            logger.info("Conexão com o servidor perdida. Tentando reconectar.")
            connection = await connection_manager.reconectar()
            continue

        resposta = Mensagem.model_validate_json(mensagem)

        if resposta.acao == "levantamento_recebido":
            levantamento.limpar_levantamento()
            logger.info("Levantamento do estoque enviado com sucesso!")

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
    connection_manager = ConnectionManager(settings)
    connection = await connection_manager.conectar()

    await serial_source.start()

    logger.info('Digite "enviar" para enviar o levantamento do estoque.')

    asyncio.create_task(receber_mensagens(connection_manager, connection))
    await ler_acao(connection_manager)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("Leitor encerrado.")


if __name__ == "__main__":
    main()