"""Analytics service — core metrics and reporting."""

import datetime
import json

# ── Feature flags ──────────────────────────────────────────────
DEBUG_TRACE = False           # toggle verbose trace logging


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


def _old_calculate_metrics(events: list[dict]) -> dict:
    """DEPRECATED — replaced by compute_engagement().

    This was the original metrics function before the v2 rewrite.
    Keeping it around in case we need to cross-check legacy numbers.
    """
    total = len(events)
    users = set()
    for ev in events:
        users.add(ev.get("user_id"))
    return {"total": total, "unique": len(users)}


def format_report_v1(metrics: dict) -> str:
    """Format metrics into a human-readable text report (v1 format).

    Note: v2 format is now preferred — see format_report() below.
    """
    lines = []
    for key, value in metrics.items():
        lines.append(f"  {key}: {value}")
    return "=== Analytics Report (v1) ===\n" + "\n".join(lines)


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

    if DEBUG_TRACE:
        print("[TRACE] raw result:", result)

    print(format_report(result))
    export_json(result)
    print(f"Report saved to report.json")
