from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

config = dotenv_values(Path(__file__).parent / "core" / ".env")

# Koneksi utama
engine = create_engine(
    config["DB_CONNECTION_URL"],
    pool_size=20,
    pool_pre_ping=True,
    pool_recycle=28800,
    max_overflow=0
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

# Koneksi Chat
chat_engine = create_engine(
    config["DB_CHAT_CONNECTION_URL"],
    pool_size=20,
    pool_pre_ping=True,
    pool_recycle=28800,
    max_overflow=0
)
ChatSessionLocal = sessionmaker(bind=chat_engine, autocommit=False, autoflush=False, future=True)

# Koneksi master_satusehat
ss_master_engine = create_engine(
    config["DB_MASTER_SATUSEHAT_CONNECTION_URL"],
    pool_size=5,
    pool_pre_ping=True,
    pool_recycle=28800,
    max_overflow=0
)
SatusehatMasterSessionLocal = sessionmaker(bind=ss_master_engine, autocommit=False, autoflush=False, future=True)

# Koneksi log
log_engine = create_engine(
    config["DB_LOG_CONNECTION_URL"],
    pool_size=5,
    pool_pre_ping=True,
    pool_recycle=28800,
    max_overflow=0
)
LogSessionLocal = sessionmaker(bind=log_engine, autocommit=False, autoflush=False, future=True)

# Base data schema
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_chat():
    db = ChatSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_ss_master():
    db = SatusehatMasterSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_log_db():
    db = LogSessionLocal()
    try:
        yield db
    finally:
        db.close()
