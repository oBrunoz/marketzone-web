from decimal import Decimal
import shutil
from typing import Dict
from fastapi import Cookie, FastAPI, Depends, HTTPException, Request, Form, UploadFile, File, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.models import Produto
from src.database.db import SessionLocal, engine, get_db
from src.schemas import produto_schema, user_schema
from src.services import crud_service
from src.services.crud_service import create_produto, get_produto, get_produtos, get_produtos_by_ids
from src.utils.util import flash, get_current_user_id
from pathlib import Path

UPLOAD_DIRECTORY = Path("src") / "static" / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="src/templates")

produto_router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}}
)

# Rota de página de cadastro
@produto_router.get('/cadastro', response_class=HTMLResponse)
async def cadastro(request: Request):

    if request.session.get('user'):
        print('pode acessar')
        return templates.TemplateResponse(
            name='produtos/cadastrar.html',
            request=request
        )
    else:
        print('Usuário não autenticado, redirecionando para a página de login')
        flash(request, "Para adicionar um produto, por favor, faça login", "green")
        # Redireciona para a página de login (substitua '/login' pela rota correta)
        return RedirectResponse(url='/login', status_code=303)


# Método POST para cadastrar o produto
@produto_router.post('/cadastro')
async def cadastrar_produto(
    request: Request,
    db: Session = Depends(get_db),
    nome: str = Form(...),
    descricao: str = Form(None),
    preco: str = Form(...),
    categoria: str = Form(...),
    rating: int = Form(None),
    imagem: UploadFile = File(None),
    user_id: int = Depends(get_current_user_id)
):
    cleaned_value = preco.replace('R$', '').replace('.', '').replace(',', '.')
    preco_decimal = Decimal(cleaned_value)

    # Verificação dos campos obrigatórios
    if not all([nome, preco, categoria]):
        flash(request, "Por favor, preencha todos os campos obrigatórios.", "red")
        return templates.TemplateResponse(
            "produtos/cadastro.html", 
            {
                "request": request,
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "categoria": categoria,
                "error_message": "Por favor, preencha os campos corretamente."
            }
        )

    # Validação para o campo nome
    if not nome.strip():
        flash(request, "Por favor, preencha o campo Nome corretamente!", "red")
        return templates.TemplateResponse(
            "produtos/cadastro.html", 
            {
                "request": request,
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "categoria": categoria,
                "error_message": "Por favor, preencha os campos corretamente."
            }
        )

    image_path = None

    if imagem and imagem.filename:
        try:
            # Salvar a imagem no diretório de uploads
            image_path = UPLOAD_DIRECTORY / imagem.filename
            # Salvando a imagem no diretório especificado
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(imagem.file, buffer)
            # Salva o caminho relativo da imagem no banco de dados
            image_path = f"static/uploads/{imagem.filename}"
        except Exception as e:
            print(f'Erro ao fazer upload da imagem. {e}')
            raise HTTPException(status_code=500, detail="Erro ao fazer upload da imagem.")
    
    try:
        # Criação do objeto ProdutoCreate
        data_produto = produto_schema.ProdutoCreate(
            nome=nome,
            descricao=descricao,
            preco=preco_decimal,
            categoria=categoria,
            avaliacao=rating if rating else 0,
            imagem=image_path,
            user_id=user_id['id']
        )

        # Chamada para o serviço CRUD para criar o produto
        db_produto = create_produto(db=db, produto=data_produto)

        if db_produto:
            print('produto cadastrado')
            return RedirectResponse("/", status_code=303)
        else:
            print('nao cadastrado')
            return templates.TemplateResponse("produtos/cadastrar.html", {"request": request})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("produtos/cadastrar.html", {"request": request})

@produto_router.post('/add-to-cart')
async def add_to_cart(request: Request, db: Session = Depends(get_db), product_id: int = Form(...)):
    produto = get_produto(db, product_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    # session_cart = request.session.get('cart_items', {})
    session_cart: Dict[str, Dict[str, int]] = request.session.get('cart_items', {})

    # Debug: print the type and contents of session_cart
    print(f"Session Cart Before: {session_cart}")
    
    # Verificar se o produto já está no carrinho e incrementar a quantidade
    if str(product_id) in session_cart:
        session_cart[str(product_id)]["quantity"] += 1
    else:
        session_cart[str(product_id)] = {
            "product_id": product_id,
            "quantity": 1,
        }
    
    total_quantity = sum(item_data['quantity'] for item_data in session_cart.values())

    request.session["total"] = total_quantity
    request.session["cart_items"] = session_cart

    return JSONResponse(status_code=200, content={
        "message": "Produto adicionado ao carrinho",
        "cart": session_cart,
        "product_id": product_id,
        "quantity": session_cart[str(product_id)]["quantity"],
        "total": total_quantity
    })

@produto_router.get('/carrinho', response_class=HTMLResponse)
async def cart(request: Request, db: Session = Depends(get_db)):
    session_cart = request.session.get("cart_items", {})
    print(session_cart)
    print(request.session.get('user', {}))

    product_ids = list(session_cart.keys())

    if not product_ids:
        return templates.TemplateResponse("produtos/carrinho.html", {"request": request, "cart_items": []})
    
    # Converte os IDs para int (já que eles foram armazenados como strings)
    product_ids = [int(pid) for pid in product_ids]

    produtos = get_produtos_by_ids(db, product_ids)

    cart_items = []
    for produto in produtos:
        pid_str = str(produto.id_produto)
        cart_items.append({
            "product_id": produto.id_produto,
            "product_name": produto.nome,
            "product_descricao": produto.descricao,
            "product_price": produto.preco,
            "product_imagem": produto.imagem,
            "quantity": session_cart[pid_str]["quantity"]
        })

    return templates.TemplateResponse("produtos/carrinho.html", {"request": request, "cart_items": cart_items})

@produto_router.post('/carrinho/deletar', response_class=HTMLResponse)
def delete_element(request: Request, item_id: int = Form(...)):
    session_cart = request.session.get("cart_items", {})
    session_total = request.session.get('total', 0)

    item_id_str = str(item_id)

    if item_id_str in session_cart:
        if session_cart[item_id_str]['quantity'] > 1:
            session_cart[item_id_str]['quantity'] -= 1
            session_total -= 1
        else:
            del session_cart[item_id_str]
            session_total -= 1

        request.session["cart_items"] = session_cart
        request.session['total'] = session_total

    return RedirectResponse('/produto/carrinho', status_code=303)

@produto_router.post('/carrinho/comprar', response_class=HTMLResponse)
async def realizar_compra(request: Request, db: Session = Depends(get_db), total_price: float = Form(...)):
    session_cart: Dict[str, Dict[str, int]] = request.session.get('cart_items', {})

    if not session_cart:
        raise HTTPException(status_code=400, detail="Carrinho está vazio")

    # Validação e atualização de estoque
    for item_id, item_data in session_cart.items():
        produto = get_produto(db, int(item_id))  # Função que busca o produto no banco
        produto.is_active = False

        db.add(produto)

    db.commit()

    # Limpa o carrinho após a compra
    request.session.pop('cart_items', None)
    request.session.pop('total', None)

    return JSONResponse({"status": "success", "message": "Compra realizada com sucesso!"})