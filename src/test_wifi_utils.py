"""Unit tests for find_weak_signals in wifi_utils."""

import pytest

from src.wifi_utils import find_weak_signals


def test_empty_list_returns_empty() -> None:
    """An empty input list should return an empty list."""
    result = find_weak_signals([])
    assert result == []


def test_all_aps_above_threshold_returns_empty() -> None:
    """No APs should be returned when all are at or above the default threshold."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 15},
        {"ap_id": "AP-02", "tx_power": 20},
        {"ap_id": "AP-03", "tx_power": 12},  # exactly at threshold — not weak
    ]
    result = find_weak_signals(aps)
    assert result == []


def test_all_aps_below_threshold_returns_all() -> None:
    """All APs should be returned when all are below the default threshold."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 5},
        {"ap_id": "AP-02", "tx_power": 8},
        {"ap_id": "AP-03", "tx_power": 11},
    ]
    result = find_weak_signals(aps)
    assert result == aps


def test_mixed_list_returns_only_weak_aps() -> None:
    """Only APs with tx_power strictly below threshold should be returned."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 5},
        {"ap_id": "AP-02", "tx_power": 15},
        {"ap_id": "AP-03", "tx_power": 11},
        {"ap_id": "AP-04", "tx_power": 20},
    ]
    result = find_weak_signals(aps)
    assert len(result) == 2
    ap_ids = [ap["ap_id"] for ap in result]
    assert "AP-01" in ap_ids
    assert "AP-03" in ap_ids


def test_ap_exactly_at_threshold_is_excluded() -> None:
    """An AP with tx_power equal to the threshold should not be included."""
    aps = [{"ap_id": "AP-01", "tx_power": 12}]
    result = find_weak_signals(aps)
    assert result == []


def test_ap_one_below_threshold_is_included() -> None:
    """An AP with tx_power one below the threshold should be included."""
    aps = [{"ap_id": "AP-01", "tx_power": 11}]
    result = find_weak_signals(aps)
    assert len(result) == 1
    assert result[0]["ap_id"] == "AP-01"


def test_ap_missing_tx_power_is_treated_as_zero() -> None:
    """An AP without a tx_power key should default to 0 and be flagged as weak."""
    aps = [{"ap_id": "AP-01", "location": "Lobby"}]
    result = find_weak_signals(aps)
    assert len(result) == 1
    assert result[0]["ap_id"] == "AP-01"


def test_custom_threshold_is_respected() -> None:
    """A custom threshold value should override the default of 12."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 18},
        {"ap_id": "AP-02", "tx_power": 25},
        {"ap_id": "AP-03", "tx_power": 19},
    ]
    result = find_weak_signals(aps, threshold=20)
    assert len(result) == 2
    ap_ids = [ap["ap_id"] for ap in result]
    assert "AP-01" in ap_ids
    assert "AP-03" in ap_ids
    assert "AP-02" not in ap_ids


def test_returns_full_ap_dicts_not_just_ids() -> None:
    """The returned items should be the original AP dicts, not modified copies."""
    ap = {"ap_id": "AP-01", "tx_power": 5, "location": "Floor 1", "band": "5 GHz"}
    result = find_weak_signals([ap])
    assert len(result) == 1
    assert result[0] == ap


def test_multiple_aps_same_tx_power_below_threshold_all_returned() -> None:
    """Multiple APs sharing the same weak tx_power should all be returned."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 8},
        {"ap_id": "AP-02", "tx_power": 8},
        {"ap_id": "AP-03", "tx_power": 8},
    ]
    result = find_weak_signals(aps)
    assert len(result) == 3


def test_zero_threshold_returns_nothing() -> None:
    """With threshold=0, no AP (including missing tx_power) should be returned."""
    aps = [
        {"ap_id": "AP-01", "tx_power": 0},
        {"ap_id": "AP-02"},  # defaults to 0
    ]
    result = find_weak_signals(aps, threshold=0)
    assert result == []


def test_negative_tx_power_below_threshold_is_included() -> None:
    """An AP with a negative tx_power should be caught as weak."""
    aps = [{"ap_id": "AP-01", "tx_power": -5}]
    result = find_weak_signals(aps)
    assert len(result) == 1
    assert result[0]["ap_id"] == "AP-01"