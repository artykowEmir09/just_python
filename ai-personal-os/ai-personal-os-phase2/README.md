# AI Personal OS

Notes, tasks, and an AI assistant, built with FastAPI + SQLite.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and try `GET /health`.
The first run creates `personal_os.db` automatically.

## Status
- [x] Phase 0: setup
- [x] Phase 1: database models
- [x] Phase 2: Notes, Tasks, Tags CRUD
- [ ] Phase 3: search and filters

## Run the tests
```bash
python -m pytest
```
