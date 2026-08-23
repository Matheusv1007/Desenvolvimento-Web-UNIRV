from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict


app = FastAPI(
    title="API de Produtos",
    description="API baseada na estrutura de produtos da Fake Store API.",
)


class Avaliacao(BaseModel):
    """Estrutura do campo rating de um produto."""

    model_config = ConfigDict(extra="forbid")

    rate: float
    count: int


class Produto(BaseModel):
    """Estrutura de um produto da Fake Store API."""

    model_config = ConfigDict(extra="forbid")

    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: Avaliacao

produtos: list[Produto] = [
    Produto(
        id=1,
        title="Fjallraven - Foldsack No. 1 Backpack",
        price=109.95,
        description="Your perfect pack for everyday use and walks in the forest.",
        category="men's clothing",
        image="https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
        rating=Avaliacao(rate=3.9, count=120),
    ),
    Produto(
        id=2,
        title="Mens Casual Premium Slim Fit T-Shirts",
        price=22.30,
        description="Slim-fitting style, contrast raglan long sleeve.",
        category="men's clothing",
        image="https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879_.jpg",
        rating=Avaliacao(rate=4.1, count=259),
    ),
    Produto(
        id=3,
        title="Mens Cotton Jacket",
        price=55.99,
        description="Great outerwear jacket for spring, autumn or winter.",
        category="men's clothing",
        image="https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
        rating=Avaliacao(rate=4.7, count=500),
    ),
]


def buscar_produto(id: int) -> Produto:
    """Busca um produto pelo ID ou responde com HTTP 404."""

    for produto in produtos:
        if produto.id == id:
            return produto

    raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.get("/produtos", response_model=list[Produto])
def listar_produtos() -> list[Produto]:
    return produtos


@app.get("/produtos/{id}", response_model=Produto)
def obter_produto(id: int) -> Produto:
    return buscar_produto(id)


@app.post(
    "/produtos",
    response_model=Produto,
    status_code=status.HTTP_201_CREATED,
)
def criar_produto(produto: Produto) -> Produto:
    print("PRODUTO RECEBIDO E VALIDADO:")
    print(produto)

    if any(item.id == produto.id for item in produtos):
        raise HTTPException(status_code=409, detail="Já existe um produto com este ID")

    produtos.append(produto)
    return produto


@app.put("/produtos/{id}", response_model=Produto)
def atualizar_produto(id: int, produto: Produto) -> Produto:
    print("PRODUTO RECEBIDO E VALIDADO:")
    print(produto)

    if produto.id != id:
        raise HTTPException(
            status_code=400,
            detail="O ID do corpo da requisição deve ser igual ao ID da URL",
        )

    for indice, item in enumerate(produtos):
        if item.id == id:
            produtos[indice] = produto
            return produto

    raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.delete("/produtos/{id}", response_model=Produto)
def excluir_produto(id: int) -> Produto:
    produto = buscar_produto(id)

    print("PRODUTO QUE SERÁ EXCLUÍDO:")
    print(produto)

    produtos.remove(produto)
    return produto
