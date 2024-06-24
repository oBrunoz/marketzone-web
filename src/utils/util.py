from fastapi import Request
from typing import Optional
import typing
import time
import bcrypt

def hash_password(password: str) -> str:
    """
    Função para gerar o hash de uma senha utilizando o algoritmo bcrypt.

    Args:
    - password (str): Senha em texto claro a ser encriptada.

    Returns:
    - str: Hash da senha encriptada.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Função para verificar se uma senha em texto claro corresponde ao hash armazenado.

    Args:
    - plain_password (str): Senha em texto claro a ser verificada.
    - hashed_password (str): Hash da senha armazenada.

    Returns:
    - bool: True se a senha corresponder ao hash, False caso contrário.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def flash(request: Request, message: typing.Any, category: str = "primary"):
    """
    Função para adicionar uma mensagem de flash à sessão do usuário.

    Args:
    - request (Request): Objeto da requisição FastAPI.
    - message (Any): Mensagem a ser exibida ao usuário.
    - category (str): Categoria da mensagem (opcional, padrão é "primary").
    """
    if "_messages" not in request.session:
        request.session["_messages"] = []
    timestamp = time.time()
    request.session["_messages"].append({"message": message, "category": category, "timestamp": timestamp})

