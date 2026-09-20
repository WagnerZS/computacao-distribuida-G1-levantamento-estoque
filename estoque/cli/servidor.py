import asyncio
import json

from estoque.config import Settings
from estoque.api.app import make_app

from tornado.platform.asyncio import AsyncIOMainLoop

import logging

settings = Settings()
logger = logging.getLogger(__name__)

async def run_server():
    logger.info("Iniciando servidor...")
    AsyncIOMainLoop().install()
    
    app = make_app()
    app.listen(settings.server_port, address=settings.server_host)

    logger.info("Servidor iniciado.")
    await asyncio.Event().wait()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    await run_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Encerrando aplicação...")