from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class BankRead(BaseModel):
	id: int
	name: str

	class Config:
		from_attributes = True


class BranchRead(BaseModel):
	ifsc: str
	branch: Optional[str] = None
	address: Optional[str] = None
	city: Optional[str] = None
	district: Optional[str] = None
	state: Optional[str] = None
	bank: BankRead

	class Config:
		from_attributes = True
