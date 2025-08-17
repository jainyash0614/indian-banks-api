import os
from contextlib import contextmanager
from typing import Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.main as main_module
from app.db import Base
from app.models import Bank, Branch


@pytest.fixture(scope="session", autouse=True)
def setup_test_app():
	# Use in-memory SQLite for speed; StaticPool to share the same connection
	test_engine = create_engine(
		"sqlite+pysqlite:///:memory:",
		future=True,
		connect_args={"check_same_thread": False},
		poolclass=StaticPool,
	)
	TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, expire_on_commit=False)

	Base.metadata.create_all(bind=test_engine)

	# Seed minimal data
	session = TestingSessionLocal()
	bank = Bank(id=123, name="Test Bank")
	session.add(bank)
	branch = Branch(
		ifsc="TEST0000001",
		bank_id=123,
		branch="Main",
		address="123 Test Street",
		city="TestCity",
		district="TestDistrict",
		state="TestState",
	)
	session.add(branch)
	session.commit()
	session.close()

	def override_get_session() -> Generator:
		session = TestingSessionLocal()
		try:
			yield session
		finally:
			session.close()

	# Override the dependency in the app to use our in-memory DB
	main_module.app.dependency_overrides[main_module.get_session] = override_get_session
	yield


@pytest.mark.asyncio
async def test_healthcheck():
	async with AsyncClient(app=main_module.app, base_url="http://test") as client:
		resp = await client.get("/healthz")
		assert resp.status_code == 200
		assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_banks():
	async with AsyncClient(app=main_module.app, base_url="http://test") as client:
		resp = await client.get("/banks")
		assert resp.status_code == 200
		banks = resp.json()
		assert isinstance(banks, list)
		assert len(banks) == 1
		assert banks[0]["name"] == "Test Bank"


@pytest.mark.asyncio
async def test_branch_by_ifsc_and_by_bank():
	async with AsyncClient(app=main_module.app, base_url="http://test") as client:
		# By IFSC
		resp = await client.get("/branches/TEST0000001")
		assert resp.status_code == 200
		branch = resp.json()
		assert branch["ifsc"] == "TEST0000001"
		assert branch["bank"]["name"] == "Test Bank"

		# By bank -> branches list
		resp2 = await client.get("/banks/123/branches")
		assert resp2.status_code == 200
		branches = resp2.json()
		assert len(branches) == 1
		assert branches[0]["ifsc"] == "TEST0000001"
