# Mini CRM: lead distribution by operators & sources

Small FastAPI service that:
- stores operators, leads, sources (bots),
- keeps routing rules (weights) per source,
- and automatically assigns new contacts to operators
  based on weights and load limits.

## Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (sync)
- SQLite (file `crm.db`)
- Uvicorn (for local run)

## How to run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
