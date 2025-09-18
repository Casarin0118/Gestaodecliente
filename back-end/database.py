# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o caminho e o nome do arquivo do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./agendamentos.db"

# Cria a "engine" do SQLAlchemy, o ponto central de comunicação com o banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões (SessionLocal) que será usada para cada transação com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é uma classe base para nossos modelos de tabela (declararemos eles em models.py)
Base = declarative_base()