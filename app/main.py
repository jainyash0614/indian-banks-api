from __future__ import annotations

import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import Base, engine, get_session, SessionLocal
from .models import Bank, Branch
from .schemas import BankRead, BranchRead
from .ingest import ingest_csv_if_needed


def init_db_and_data(session: Session) -> None:
	Base.metadata.create_all(bind=engine)
	ingest_csv_if_needed(session)


app = FastAPI(title="Indian Banks API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
	if os.environ.get("SKIP_STARTUP") == "1":
		return
	# Open a session directly; do not use the dependency generator here
	session = SessionLocal()
	try:
		init_db_and_data(session)
		session.commit()
	finally:
		session.close()


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
	return RedirectResponse(url="/docs")


# REST Endpoints

@app.get("/banks", response_model=List[BankRead])
def list_banks(q: Optional[str] = Query(default=None, description="Search by bank name"), session: Session = Depends(get_session)) -> List[BankRead]:
	query = select(Bank)
	if q:
		query = query.where(Bank.name.ilike(f"%{q}%"))
	banks = session.execute(query.order_by(Bank.name)).scalars().all()
	return banks


@app.get("/branches/{ifsc}", response_model=BranchRead)
def get_branch_by_ifsc(ifsc: str, session: Session = Depends(get_session)) -> BranchRead:
	branch = session.get(Branch, ifsc)
	if not branch:
		raise HTTPException(status_code=404, detail="Branch not found")
	# Eager load bank via access
	_ = branch.bank
	return branch


@app.get("/banks/{bank_id}/branches", response_model=List[BranchRead])
def list_branches_for_bank(
	bank_id: int,
	branch: Optional[str] = Query(default=None, description="Filter by branch name contains"),
	city: Optional[str] = Query(default=None),
	state: Optional[str] = Query(default=None),
	session: Session = Depends(get_session),
) -> List[BranchRead]:
	# Validate bank exists
	bank = session.get(Bank, bank_id)
	if not bank:
		raise HTTPException(status_code=404, detail="Bank not found")

	query = select(Branch).where(Branch.bank_id == bank_id)
	if branch:
		query = query.where(Branch.branch.ilike(f"%{branch}%"))
	if city:
		query = query.where(Branch.city.ilike(f"%{city}%"))
	if state:
		query = query.where(Branch.state.ilike(f"%{state}%"))

	branches = session.execute(query.order_by(Branch.branch)).scalars().all()
	# Eager load bank in response
	for b in branches:
		_ = b.bank
	return branches


@app.get("/healthz")
def healthcheck() -> dict:
	return {"status": "ok"}


# Uvicorn entrypoint
if __name__ == "__main__":
	import uvicorn

	host = os.environ.get("HOST", "0.0.0.0")
	port = int(os.environ.get("PORT", "8000"))
	uvicorn.run("app.main:app", host=host, port=port, reload=True)
