from pydantic import BaseModel

from estoque.domain.produto.enitity import Produto, ProdutoLevantamento


class Mensagem(BaseModel):
    acao: str
    produto: Produto | None = None
    produtos: list[ProdutoLevantamento] | None = None