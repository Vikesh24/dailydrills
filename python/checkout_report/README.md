━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PYTHON DRILL · Session #1 · L1 / T1 — Scoped
Concept: Core types — lists, dicts, sets, tuples, comprehensions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Build an order-deduplication + SKU-frequency reporter for checkout events

Background
───────────

Swiggy Instamart's checkout event pipeline occasionally emits duplicate order records (network retries at the edge). Before events reach the warehouse loader, a lightweight in-memory pass needs to dedupe and summarize a batch of ~50K records per minute.

What to Build
──────────────

Take a list of order event dicts (fields: order_id, sku, qty, city) and return the deduplicated list, keyed by order_id (keep first occurrence).
Build a dict mapping each SKU to total quantity sold across the deduped batch.
Build a set of distinct cities present in the batch.
Return the top 3 SKUs by quantity as a list of (sku, qty) tuples, sorted descending — ties broken by SKU name ascending.
Use at least one comprehension (list, dict, or set) meaningfully — not cosmetically.

Constraints
────────────

Python stdlib only.
Input is a plain list of dicts — don't assume a DataFrame or external library.
Must handle an empty input list without raising.