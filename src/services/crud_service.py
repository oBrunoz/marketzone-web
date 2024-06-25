from typing import List
from sqlalchemy.orm import Session
from src.models.Produto import Produto
from src.models.User import User
from datetime import datetime

from src.schemas import user_schema
from src.schemas.produto_schema import ProdutoCreate
from src.utils.util import hash_password

# PRODUTO

def get_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id_produto == produto_id).first()

def get_produtos_by_ids(db: Session, produto_ids: List[int]) -> List[Produto]:
    # Filtra produtos que têm um ID dentro da lista fornecida
    return db.query(Produto).filter(Produto.id_produto.in_(produto_ids)).all()

def get_produtos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Produto).filter(Produto.is_active == True).offset(skip).limit(limit).all()

def create_produto(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, nome: str, descricao: str, preco: float, categoria: str, imagem: str, avaliacao: int):
    db_produto = db.query(Produto).filter(Produto.id_produto == produto_id).first()
    if db_produto:
        db_produto.nome = nome
        db_produto.descricao = descricao
        db_produto.preco = preco
        db_produto.categoria = categoria
        db_produto.imagem = imagem
        db_produto.avaliacao = avaliacao
        db.commit()
        db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.id_produto == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto

# USER

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = hash_password(user.hashed_password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, username: str, email: str, full_name: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = username
        db_user.email = email
        db_user.full_name = full_name
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
