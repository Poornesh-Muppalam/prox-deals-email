import json
from pathlib import Path
from prox.db import get_client

def seed_users(users_path: str = "data/users.json") -> int:
    sb = get_client()
    users = json.loads(Path(users_path).read_text())

    for u in users:
        sb.table("users").upsert(
            {
                "name": u.get("name", ""),
                "email": u["email"],
                "preferred_retailers": u.get("preferred_retailers", []),
            },
            on_conflict="email",
        ).execute()

    return len(users)
