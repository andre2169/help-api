from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco
DATABASE_URL = "postgresql://user:password@localhost:5432/help_api"

# Engine: gerencia a conexão com o banco
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal: cria sessões para conversar com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os models
Base = declarative_base()
