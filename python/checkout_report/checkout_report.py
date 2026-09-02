"""
./checkout_report.py

A simple script to deduplicate the order events
"""

from typing import Any


def summarize_batch(events_list: list[dict]) -> dict:
    """
    Deduplicates the events data and summarizes the events

    Args:
        events_list - List of events data
    
    Returns:
        A dict of summarized events with deduped events data, total skus' ordered, distinct cities, top selling sku
    """
    seen = set()
    distinct_events = []

    for event in events_list:
        if event["order_id"] not in seen:
            seen.add(event["order_id"])
            distinct_events.append(event)

    sku_totals: dict[str, int] = {}

    cities: set[str] = {event["city"] for event in distinct_events}

    for event in distinct_events:
        sku_totals[event["sku"]] = sku_totals.get(event["sku"], 0) + event["qty"]

    top_skus = sorted(sku_totals.items(), key=lambda item: (-item[1], item[0]))

    return {
        "deduped": distinct_events,
        "sku_totals": sku_totals,
        "cities": cities,
        "top_skus": top_skus[:3]
    }


if __name__ == "__main__":
    TEST_DATA = [
        {"order_id": 1, "sku": "SKU-001", "qty": 2, "city": "Seattle"},
        {"order_id": 2, "sku": "SKU-002", "qty": 1, "city": "Portland"},
        {"order_id": 1, "sku": "SKU-001", "qty": 2, "city": "Seattle"},
        {"order_id": 3, "sku": "SKU-003", "qty": 4, "city": "Denver"},
        {"order_id": 2, "sku": "SKU-002", "qty": 1, "city": "Portland"},
        {"order_id": 4, "sku": "SKU-004", "qty": 1, "city": "Austin"},
    ]

    print(summarize_batch(TEST_DATA))