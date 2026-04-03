"""WiFi site-survey utilities for the Copilot features demo."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "ap_inventory.json"

# Channel planning constants
VALID_STATUSES = {"planned", "deployed", "offline", "decommissioned"}
VALID_BANDS = {"2.4 GHz", "5 GHz", "6 GHz"}
VALID_SIGNAL_QUALITIES = {"good", "marginal", "critical"}


def load_aps(path: Path | None = None) -> list[dict]:
    """Load access points from the JSON data file."""
    path = path or DATA_FILE
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_weak_signals(aps: list[dict], threshold: int = 12) -> list[dict]:
    """Return APs whose tx_power is below the given threshold.

    Args:
        aps: List of AP dicts to filter.
        threshold: Minimum acceptable tx_power in dBm. Defaults to 12.

    Returns:
        A list of AP dicts with tx_power below the threshold.
    """
    return [ap for ap in aps if ap.get("tx_power", 0) < threshold]


def filter_aps_by_band(aps: list[dict], band: str) -> list[dict]:
    """Return APs operating on the specified frequency band.

    Args:
        aps: List of AP dicts to filter.
        band: The band to filter by (e.g., '5 GHz').

    Returns:
        A list of AP dicts whose 'band' field matches.

    Raises:
        ValueError: If band is not a valid value.
    """
    if band not in VALID_BANDS:
        raise ValueError(f"Invalid band '{band}'. Must be one of {VALID_BANDS}")
    return [ap for ap in aps if ap.get("band") == band]


def filter_aps_by_status(aps: list[dict], status: str) -> list[dict]:
    """Return APs matching the given deployment status.

    Args:
        aps: List of AP dicts to filter.
        status: The status to filter by.

    Returns:
        A list of AP dicts whose 'status' field matches.

    Raises:
        ValueError: If status is not a valid value.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}")
    return [ap for ap in aps if ap.get("status") == status]


def count_by_status(aps: list[dict]) -> dict[str, int]:
    """Return a dict of AP counts grouped by status."""
    counts: dict[str, int] = {}
    for ap in aps:
        s = ap.get("status", "unknown")
        counts[s] = counts.get(s, 0) + 1
    return counts


def count_by_band(aps: list[dict]) -> dict[str, int]:
    """Return a dict of AP counts grouped by band."""
    counts: dict[str, int] = {}
    for ap in aps:
        b = ap.get("band", "unknown")
        counts[b] = counts.get(b, 0) + 1
    return counts


def summary(aps: list[dict]) -> dict:
    """Return a dict summarising AP counts by status, band, and signal quality."""
    by_status = count_by_status(aps)
    by_band = count_by_band(aps)
    by_quality: dict[str, int] = {}
    for ap in aps:
        q = ap.get("signal_quality", "N/A")
        by_quality[q] = by_quality.get(q, 0) + 1
    return {
        "total": len(aps),
        "by_status": by_status,
        "by_band": by_band,
        "by_signal_quality": by_quality,
    }


if __name__ == "__main__":
    aps = load_aps()
    s = summary(aps)
    print(f"AP Inventory Summary")
    print(f"{'='*40}")
    print(f"Total APs: {s['total']}\n")

    print("By Status:")
    for status, count in sorted(s["by_status"].items()):
        print(f"  {status:<20} {count}")

    print("\nBy Band:")
    for band, count in sorted(s["by_band"].items()):
        print(f"  {band:<20} {count}")

    print("\nBy Signal Quality:")
    for quality, count in sorted(s["by_signal_quality"].items()):
        print(f"  {quality:<20} {count}")

    weak = find_weak_signals(aps)
    if weak:
        print(f"\nWeak Signal APs (tx_power < 12 dBm):")
        for ap in weak:
            print(f"  {ap['ap_id']} — {ap['location']} (tx_power: {ap['tx_power']} dBm)")
