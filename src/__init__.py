from fastapi import FastAPI, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.schemas import user_schema
from .database.db import engine, get_db, Base
from .services import crud_service
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.utils.util import flash, hash_password
from src.views.routes import produto_router
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

# Configuração do banco de dados
Base.metadata.create_all(bind=engine)

# Instanciação da aplicação FastAPI
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='secret_key')

# @app.middleware("http")
# async def some_middleware(request: Request, call_next):
#     response = await call_next(request)
#     session = request.cookies.get('session')
#     if session:
#         response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)
#     return response

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configuração de templates com JINJA2
templates = Jinja2Templates(directory="src/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Registra o roteador de usuário
app.include_router(produto_router)

# Importação de rotas
from src.views import routes

# Rota principal - HOME
@app.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    select_produtos = crud_service.get_produtos(db)

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "produtos": select_produtos}
    )

@app.get('/cadastro', response_class=HTMLResponse)
async def cadastro_user(request: Request):
    return templates.TemplateResponse("cadastro_user.html", {"request": request})

@app.post('/cadastro', response_class=HTMLResponse)
async def cadastrar_user(request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), hashed_password: str = Form(...)):
    existing_user = crud_service.get_user_by_email(db, email)
    if existing_user:
        return 'Usuario ja existente'
    
    data_user = user_schema.UserCreate(
        username=username, email=email, hashed_password=hashed_password
    )

    try:
        db_user = crud_service.create_user(db, data_user)
    except Exception as e:
        # Log do erro para debug (opcional)
        print(f"Erro ao criar usuário: {e}")
        flash(request, "Houve um erro ao cadastrar usuário. Tente novamente ou contate um administrador.", "red")
        return templates.TemplateResponse("cadastro_user.html", {"request": request})

    if db_user:
        return RedirectResponse("/login", status_code=303)
    else:
        flash(request, "Houve um erro ao cadastrar usuário. Tente novamente ou contate um administrador.", "red")
        return templates.TemplateResponse("cadastro_user.html", {"request": request})

@app.get('/login', response_class=HTMLResponse)
async def login_user(request: Request):
    return templates.TemplateResponse("login_user.html", {"request": request})

@app.post('/logar', response_class=HTMLResponse)
async def logar_user(request: Request, db: Session = Depends(get_db), email: str = Form(...), hashed_password: str = Form(...)):
    user = crud_service.get_user_by_email(db, email)
    if not user or not pwd_context.verify(hashed_password, user.hashed_password):
        flash(request, "Email ou senha incorretos. Por favor, tente novamente", "red")
        return templates.TemplateResponse("login_user.html", {"request": request})
        # raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    request.session["user"] = {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }
    
    return RedirectResponse('/', 303)

@app.get("/logout")
async def logout(request: Request):
    if "user" in request.session:
        del request.session["user"]

    return RedirectResponse('/', status_code=303)

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    user_data = crud_service.get_user(db, user['id'])

    return templates.TemplateResponse("profile.html", {"request": request, "user_data": user_data})

@app.post("/update_profile", response_class=HTMLResponse)
async def update_profile(request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Validação dos dados (exemplo simples)
    if not username or not email:
        raise HTTPException(status_code=400, detail="Username e email são obrigatórios")
    
    # Atualização dos dados do usuário no banco de dados
    user = request.session.get("user")
    if not user:
        flash(request, "Usuário não autenticado", 'green')
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    # Consulta para buscar o usuário no banco de dados
    db_user = crud_service.get_user(db, user['id'])
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado no banco de dados")

    # Atualiza os campos do usuário com os novos dados
    db_user.username = username
    db_user.email = email
    
    # Verifica se a senha foi fornecida e atualiza apenas se estiver presente
    if password:
        db_user.hashed_password = hash_password(password)
    
    # Persiste as alterações no banco de dados
    db.commit()

    # Atualiza a sessão com os novos dados do usuário (opcional)
    request.session["user"] = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email
    }

    return RedirectResponse("/", status_code=303)
