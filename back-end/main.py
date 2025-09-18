# main.py - ORDEM CORRIGIDA

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models
from database import SessionLocal, engine
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

# PASSO 1: Criar a aplicação
app = FastAPI()

# PASSO 2: Configurar a aplicação (CORS)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class ClienteBase(BaseModel):
    nome: str
    endereco: str
    telefone: str
    descricao: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True

# --- Dependência para obter a sessão do banco ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PASSO 3: Definir os endpoints (rotas) da aplicação

@app.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.get("/clientes/", response_model=List[Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def update_cliente(cliente_id: int, cliente_atualizado: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db_cliente.nome = cliente_atualizado.nome
    db_cliente.endereco = cliente_atualizado.endereco
    db_cliente.telefone = cliente_atualizado.telefone
    db_cliente.descricao = cliente_atualizado.descricao

    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente