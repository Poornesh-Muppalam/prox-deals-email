from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from prox.db import get_client
from prox.ingest import ingest_deals
from prox.users_seed import seed_users
from prox.email_template import render_html, render_text


def _top6_grouped(deals: List[dict]) -> Dict[str, List[dict]]:
    deals_sorted = sorted(deals, key=lambda d: float(d["price"]))
    top = deals_sorted[:6]
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for d in top:
        grouped[d["retailer_name"]].append(d)
    return dict(grouped)


def run_send_weekly_dryrun() -> int:
    sb = get_client()

    # 1) Ingest deals
    ingest_deals("data/deals.json")

    # 2) Seed users
    seed_users("data/users.json")

    # 3) Generate previews
    users = sb.table("users").select("name,email,preferred_retailers").execute().data

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    generated = 0

    for u in users:
        preferred = u.get("preferred_retailers") or []
        if not preferred:
            continue

        # retailers for preferred names
        r_rows = sb.table("retailers").select("id,name").in_("name", preferred).execute().data
        retailer_ids = [r["id"] for r in r_rows]
        id_to_name = {r["id"]: r["name"] for r in r_rows}
        if not retailer_ids:
            continue

        # deals for those retailers
        deal_rows = (
            sb.table("deals")
            .select("price,start_date,end_date,retailer_id,product_id")
            .in_("retailer_id", retailer_ids)
            .execute()
            .data
        )
        if not deal_rows:
            continue

        # products for those deals
        pids = list({d["product_id"] for d in deal_rows})
        p_rows = sb.table("products").select("id,name,size,category").in_("id", pids).execute().data
        pid_map = {p["id"]: p for p in p_rows}

        normalized = []
        for d in deal_rows:
            p = pid_map.get(d["product_id"], {})
            normalized.append(
                {
                    "retailer_name": id_to_name.get(d["retailer_id"], "Unknown"),
                    "product_name": p.get("name", "Unknown product"),
                    "size": p.get("size", ""),
                    "category": p.get("category", ""),
                    "price": d["price"],
                    "start_date": d["start_date"],
                    "end_date": d["end_date"],
                }
            )

        grouped = _top6_grouped(normalized)

        html = render_html(u.get("name", ""), grouped)
        text = render_text(u.get("name", ""), grouped)

        safe_email = u["email"].replace("@", "_at_").replace(".", "_")
        (out_dir / f"{safe_email}.html").write_text(html, encoding="utf-8")
        (out_dir / f"{safe_email}.txt").write_text(text, encoding="utf-8")

        generated += 1

    return generated
