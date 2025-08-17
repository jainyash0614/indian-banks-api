from __future__ import annotations

from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .db import Base


class Bank(Base):
	__tablename__ = "banks"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
	name: Mapped[str] = mapped_column(String(49), nullable=False, index=True)

	branches: Mapped[list["Branch"]] = relationship("Branch", back_populates="bank", cascade="all, delete-orphan")

	def __repr__(self) -> str:
		return f"Bank(id={self.id}, name={self.name})"


class Branch(Base):
	__tablename__ = "branches"

	ifsc: Mapped[str] = mapped_column(String(11), primary_key=True)
	bank_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("banks.id"), index=True, nullable=False)
	branch: Mapped[str] = mapped_column(String(74), index=True)
	address: Mapped[str] = mapped_column(String(195))
	city: Mapped[str] = mapped_column(String(50), index=True)
	district: Mapped[str] = mapped_column(String(50), index=True)
	state: Mapped[str] = mapped_column(String(26), index=True)

	bank: Mapped[Bank] = relationship("Bank", back_populates="branches")

	__table_args__ = (
		Index("ix_branches_bank_branch", "bank_id", "branch"),
		Index("ix_branches_city_state", "city", "state"),
	)
