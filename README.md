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

```text
prox-deals-email/
├── prox/
│ ├── **main**.py           # Python module entrypoint (python -m prox)
│ ├── cli.py                # CLI command routing
│ ├── config.py             # Environment variable loading
│ ├── db.py                 # Supabase client setup
│ ├── ingest.py             # Deal ingestion & deduplication
│ ├── send_weekly.py        # Weekly orchestration logic
│ └── email_template.py     # HTML + plain-text email rendering
│
├── data/
│ ├── deals.json            # Sample grocery deals
│ └── users.json            # Sample users & preferences
│
├── output/                 # Generated email previews (gitignored)
│
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Database Schema (High-Level Diagram)

```text
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
```

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

## Run Instructions

This project is executed via a single CLI command that runs the entire weekly pipeline end to end.

### Prerequisites

```bash
- Before running the project, ensure that:

- The virtual environment is activated

- Dependencies are installed

- A .env file exists (created from .env.example)

- The Supabase database schema from schema.sql has been applied

```

### Run weekly pipeline

```text

python -m prox send-weekly

```

### What This Command Does

```bash

1. Loads environment variables from .env

2. Ingests grocery deals from data/deals.json

3. Normalizes and deduplicates deal records

4. Stores structured data in Supabase (Postgres)

5. Matches deals to users based on preferred retailers

6. Sorts deals by lowest price

7. Selects the top deals per user

8. Groups deals by retailer

9. Generates branded HTML and plain-text email previews

10. Writes the generated previews to the output/ directory

```

### Output

```text

After successful execution, you will see output similar to:

```

```bash

Generated 3 email previews in ./output/

```

```text

Generated files are written to:

```

```bash

output/

```

### Rerunning the pipeline

```bash

python -m prox send-weekly

```

```text

Each execution regenerates fresh email previews based on the current data.

```

```

```
