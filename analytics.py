"""Analytics service — core metrics and reporting."""

import datetime
import json


def compute_engagement(events: list[dict]) -> dict:
    """Return engagement metrics for a list of user events."""
    if not events:
        return {"total": 0, "unique_users": 0, "avg_per_user": 0.0}

    user_counts: dict[str, int] = {}
    for ev in events:
        uid = ev.get("user_id", "anonymous")
        user_counts[uid] = user_counts.get(uid, 0) + 1

    total = sum(user_counts.values())
    unique = len(user_counts)
    return {
        "total": total,
        "unique_users": unique,
        "avg_per_user": round(total / unique, 2) if unique else 0.0,
    }


# ── Dead code candidate 2 (MEDIUM confidence) ─────────────────
# Has a v1 suffix suggesting it's superseded, but the function
# is technically still importable and could be used externally.
def format_report_v1(metrics: dict) -> str:
    """Format metrics into a plain-text report (v1 layout)."""
    lines = []
    for key, value in metrics.items():
        lines.append(f"  {key}: {value}")
    return "=== Analytics Report ===\n" + "\n".join(lines)


# ── Dead code candidate 3 (LOW confidence) ────────────────────
# Helper that looks unused in this file but could plausibly be
# called by external code or tests. Not obviously dead.
def summarize_top_pages(events: list[dict], limit: int = 5) -> list[tuple[str, int]]:
    """Return the top pages by event count."""
    page_counts: dict[str, int] = {}
    for ev in events:
        page = ev.get("page", "/")
        page_counts[page] = page_counts.get(page, 0) + 1
    ranked = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
    return ranked[:limit]


def format_report(metrics: dict) -> str:
    """Format metrics into a human-readable text report (current)."""
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    header = f"Analytics Report — {ts}"
    lines = [header, "=" * len(header)]
    for key, value in metrics.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def export_json(metrics: dict, path: str = "report.json") -> str:
    """Export metrics to JSON file."""
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    return path


# ── Main entry point ──────────────────────────────────────────
if __name__ == "__main__":
    sample_events = [
        {"user_id": "u1", "action": "click", "page": "/home"},
        {"user_id": "u2", "action": "scroll", "page": "/pricing"},
        {"user_id": "u1", "action": "click", "page": "/docs"},
        {"user_id": "u3", "action": "signup", "page": "/register"},
        {"user_id": "u2", "action": "click", "page": "/home"},
    ]

    result = compute_engagement(sample_events)
    print(format_report(result))
    export_json(result)
    print("Report saved to report.json")
