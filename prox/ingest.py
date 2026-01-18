from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

from dateutil.parser import isoparse

from prox.db import get_client


@dataclass(frozen=True)
class DealIn:
    retailer: str
    product: str
    size: str
    price: float
    start: date
    end: date
    category: str


def _load_deals(path: Path) -> List[DealIn]:
    raw = json.loads(path.read_text())
    deals: List[DealIn] = []
    for row in raw:
        deals.append(
            DealIn(
                retailer=str(row["retailer"]).strip(),
                product=str(row["product"]).strip(),
                size=str(row.get("size") or "").strip(),
                price=float(row["price"]),
                start=isoparse(row["start"]).date(),
                end=isoparse(row["end"]).date(),
                category=str(row.get("category") or "").strip(),
            )
        )
    return deals


def ingest_deals(deals_path: str = "data/deals.json") -> Dict[str, int]:
    """
    Ingest deals JSON into Supabase tables: retailers, products, deals.
    Dedupe enforced by DB constraints:
      - retailers unique(name)
      - products unique(name, size, category)
      - deals unique(retailer_id, product_id, start_date)
    """
    sb = get_client()
    deals = _load_deals(Path(deals_path))

    retailer_id_cache: Dict[str, int] = {}
    product_id_cache: Dict[Tuple[str, str, str], int] = {}

    retailers_upserted = 0
    products_upserted = 0
    deals_upserted = 0

    for d in deals:
        # Retailer
        if d.retailer in retailer_id_cache:
            retailer_id = retailer_id_cache[d.retailer]
        else:
            sb.table("retailers").upsert({"name": d.retailer}, on_conflict="name").execute()
            r = sb.table("retailers").select("id").eq("name", d.retailer).single().execute()
            retailer_id = int(r.data["id"])
            retailer_id_cache[d.retailer] = retailer_id
            retailers_upserted += 1

        # Product
        pkey = (d.product, d.size, d.category)
        if pkey in product_id_cache:
            product_id = product_id_cache[pkey]
        else:
            sb.table("products").upsert(
                {"name": d.product, "size": d.size, "category": d.category},
                on_conflict="name,size,category",
            ).execute()
            p = (
                sb.table("products")
                .select("id")
                .eq("name", d.product)
                .eq("size", d.size)
                .eq("category", d.category)
                .single()
                .execute()
            )
            product_id = int(p.data["id"])
            product_id_cache[pkey] = product_id
            products_upserted += 1

        # Deal (dedupe on retailer_id + product_id + start_date)
        sb.table("deals").upsert(
            {
                "retailer_id": retailer_id,
                "product_id": product_id,
                "price": d.price,
                "start_date": d.start.isoformat(),
                "end_date": d.end.isoformat(),
            },
            on_conflict="retailer_id,product_id,start_date",
        ).execute()
        deals_upserted += 1

    return {
        "retailers_upserted": retailers_upserted,
        "products_upserted": products_upserted,
        "deals_upserted": deals_upserted,
    }
