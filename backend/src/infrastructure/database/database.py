from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./salao_da_leila.db"

# connect_args={"check_same_thread": False} Permitir que o FastAPI trabalhe de forma assíncrona com múltiplas threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_banco_de_dados():
    """Gera as tabelas fisicamente no arquivo .db caso elas não existam."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Context Manager Generator que abre uma sessão do banco para a requisição 
    e garante o fechamento automático após o término do fluxo."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()