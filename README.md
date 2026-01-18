# Prox – Weekly Grocery Deals Email Pipeline (Track A)

This project implements an end-to-end backend pipeline that ingests grocery deals, matches them to user preferences, and generates personalized weekly email previews using a CLI-driven workflow.

It demonstrates how a production-style scheduled backend job could be built for a consumer-facing product.

---

## What This Project Does (High-Level)

1. Ingests grocery deal data from external sources (simulated via JSON)
2. Normalizes and deduplicates deals
3. Stores structured data in a relational database (Supabase / Postgres)
4. Matches deals to users based on preferred retailers
5. Sorts deals by lowest price and selects top deals per user
6. Generates branded HTML and plain-text email previews
7. Exposes the entire workflow via a single CLI command

---

## Features

- Deal ingestion with normalization and deduplication
- Relational data modeling in Postgres (Supabase)
- User preference–based filtering
- Price-based ranking and selection
- Grouping by retailer for readability
- Branded HTML and plain-text email rendering
- CLI command to run the full weekly workflow
- Safe dry-run mode (no real emails sent)

---

## Tech Stack

- **Python**
- **Supabase** (Postgres + REST API)
- **dotenv** for environment configuration
- **CLI execution** (`python -m prox send-weekly`)

---

## Project Structure

<details>
<summary>📂 Click to view Project Structure</summary>

prox-deals-email/
├── prox/
│ ├── data/
│ │ ├── deals.json # Sample grocery deals
│ │ └── users.json # Sample users & retailer preferences
│ ├── output/ # Generated email previews (gitignored)
│ ├── cli.py # CLI command routing
│ ├── config.py # Environment variable loading
│ ├── db.py # Supabase client setup
│ ├── email_template.py # HTML + plain-text email rendering
│ ├── ingest.py # Deal ingestion & deduplication logic
│ ├── main.py # Python module entrypoint (python -m prox)
│ └── send_weekly.py # Weekly orchestration workflow
├── .env.example # Environment variable template
├── .gitignore # Git ignore rules
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── schema.sql # Postgres database schema

---

</details>

## Database Schema (High-Level Diagram)

users
├── id (PK)
├── email
└── name

retailers
├── id (PK)
└── name

deals
├── id (PK)
├── retailer_id (FK → retailers.id)
├── name
├── price
├── unit
├── size
├── start_date
└── end_date

user_retailer_preferences
├── user_id (FK → users.id)
└── retailer_id (FK → retailers.id)

---

## Environment Variables

Create a `.env` file using `.env.example` as a reference.

| Variable                  | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| SUPABASE_URL              | Supabase Project URL                                           |
| SUPABASE_SERVICE_ROLE_KEY | Server-side key used to bypass RLS                             |
| FROM_EMAIL                | Label used in email previews (e.g. `Prox <weekly@prox.local>`) |

> **Note:** `.env` is intentionally ignored by git for security.

---

## Setup Instructions

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


```
