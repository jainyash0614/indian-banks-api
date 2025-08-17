from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase, Session


DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///banks.db")


class Base(DeclarativeBase):
	pass


engine = create_engine(
	DATABASE_URL,
	echo=False,
	future=True,
)

SessionLocal = scoped_session(
	sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
)


def get_session() -> Generator[Session, None, None]:
	session: Session = SessionLocal()
	try:
		yield session
		session.commit()
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()
