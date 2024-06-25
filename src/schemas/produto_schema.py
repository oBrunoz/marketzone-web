from decimal import Decimal
from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

# Defina o schema Pydantic para Produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal
    categoria: Optional[str] = None
    imagem: Optional[str] = None
    avaliacao: Optional[int] = None
    is_active: Optional[bool] = True
    user_id: Optional[int]

# Schema para a criação de um novo Produto
class ProdutoCreate(ProdutoBase):
    pass

# Schema para a atualização de um Produto existente
class ProdutoUpdate(ProdutoBase):
    pass

# Schema Pydantic para Produto que inclui informações do usuário relacionado
class Produto(ProdutoBase):
    id_produto: int
    data_criacao: Optional[datetime] = datetime.utcnow()
    user_id: Optional[int]

    class Config:
        from_attributes = True
