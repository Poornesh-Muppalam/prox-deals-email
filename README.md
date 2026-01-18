# Prox – Weekly Grocery Deals Email Pipeline (Track A)

This project implements a backend pipeline that ingests grocery deals, matches them to user preferences, and generates personalized weekly email previews via a CLI-driven workflow.

It demonstrates an end-to-end backend system similar to a production scheduled job.

---

## Features

- Ingest grocery deals with normalization and deduplication
- Store data in Supabase (Postgres)
- Filter deals by user preferred retailers
- Sort by lowest price and select top 6 deals per user
- Group deals by retailer
- Generate branded HTML and plain-text email previews
- CLI command to run the full weekly workflow

---

## Tech Stack

- Python
- Supabase (Postgres + REST)
- dotenv
- CLI (`python -m prox send-weekly`)

---

## Project Structure

- `prox/__main__.py` – module entrypoint
- `prox/cli.py` – CLI command routing
- `prox/config.py` – environment loading
- `prox/db.py` – Supabase client
- `prox/ingest.py` – deal ingestion and deduplication
- `prox/send_weekly.py` – weekly orchestration logic
- `prox/email_template.py` – HTML and text email rendering
- `data/` – sample deals and users
- `schema.sql` – database schema
- `output/` – generated email previews (ignored by git)

---

## Setup

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
