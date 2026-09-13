from pathlib import Path

import pandas as pd
import pytest

from canary_demo.data import filter_events, island_for, load_events


def test_sample_contains_official_events() -> None:
    events = load_events()
    assert len(events) == 5
    assert events["event_id"].str.startswith("es").all()
    assert events["source_url"].str.contains("ign.es").all()


def test_events_are_sorted_newest_first() -> None:
    assert load_events()["occurred_at"].is_monotonic_decreasing


def test_island_classification() -> None:
    assert island_for(28.27, -16.60) == "Tenerife"
    assert island_for(28.10, -15.60) == "Gran Canaria"


def test_filter_returns_only_selected_island() -> None:
    events = pd.DataFrame(
        {
            "island": ["Tenerife", "Gran Canaria", "Tenerife"],
            "magnitude": [2.1, 2.3, 2.5],
        }
    )
    filtered = filter_events(events, "Tenerife")
    assert filtered["island"].tolist() == ["Tenerife", "Tenerife"]


def test_missing_columns_are_rejected(tmp_path: Path) -> None:
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("event_id;magnitude\nes1;2.1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing CSV columns"):
        load_events(invalid_csv)
