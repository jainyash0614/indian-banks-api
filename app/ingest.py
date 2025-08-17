from __future__ import annotations

import csv
import os
from pathlib import Path

from sqlalchemy.orm import Session

from .models import Bank, Branch


DATA_CSV = Path(__file__).resolve().parent.parent / "indian_banks" / "bank_branches.csv"


def database_is_empty(session: Session) -> bool:
	bank_count = session.query(Bank).count()
	branch_count = session.query(Branch).count()
	return bank_count == 0 or branch_count == 0


def ingest_csv_if_needed(session: Session, csv_path: str | os.PathLike | None = None) -> None:
	csv_file = Path(csv_path) if csv_path else DATA_CSV
	if not csv_file.exists():
		raise FileNotFoundError(f"CSV file not found at {csv_file}")

	if not database_is_empty(session):
		return

	# Preload existing bank ids (empty DB on first run, but safe on reruns)
	existing_bank_ids = {row[0] for row in session.query(Bank.id).all()}
	seen_bank_ids = set(existing_bank_ids)

	with csv_file.open("r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			bank_id = int(row["bank_id"]) if row.get("bank_id") else None
			bank_name = row.get("bank_name") or ""
			if bank_id is None:
				continue

			# Insert bank only once per id
			if bank_id not in seen_bank_ids:
				session.add(Bank(id=bank_id, name=bank_name))
				seen_bank_ids.add(bank_id)

			# Insert branch if not present
			ifsc = row["ifsc"]
			if session.get(Branch, ifsc) is None:
				session.add(
					Branch(
						ifsc=ifsc,
						bank_id=bank_id,
						branch=row.get("branch") or None,
						address=row.get("address") or None,
						city=row.get("city") or None,
						district=row.get("district") or None,
						state=row.get("state") or None,
					)
				)
	# Commit happens by caller
