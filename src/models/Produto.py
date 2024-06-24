from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db import Base

class Produto(Base):
    __tablename__ = 'produtos'

    id_produto = Column(Integer, primary_key=True)
    nome = Column(String, index=True)
    descricao = Column(String(255))
    preco = Column(Numeric(10, 2))
    categoria = Column(String)
    imagem = Column(String)
    avaliacao = Column(Integer)
    data_criacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="produtos")