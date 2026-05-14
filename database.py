import os

from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


# =========================
# LOAD ENV
# =========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# =========================
# CONTACT TABLE
# =========================

class Contact(Base):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True)

    email = Column(String, unique=True)


# =========================
# MEETING TABLE
# =========================

class Meeting(Base):

    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)

    person = Column(String)

    time = Column(String)


# =========================
# REQUEST HISTORY TABLE
# =========================

class RequestHistory(Base):

    __tablename__ = "request_history"

    id = Column(Integer, primary_key=True, index=True)

    user_input = Column(Text)

    plan = Column(Text)

    results = Column(Text)

    status = Column(String)

    success_count = Column(Integer)

    failure_count = Column(Integer)

    execution_time = Column(Float)


# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)