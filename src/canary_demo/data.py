from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = PROJECT_ROOT / "data" / "sample_earthquakes.csv"

ISLAND_CENTERS: dict[str, tuple[float, float]] = {
    "El Hierro": (27.75, -18.00),
    "La Palma": (28.68, -17.85),
    "La Gomera": (28.12, -17.23),
    "Tenerife": (28.27, -16.60),
    "Gran Canaria": (28.10, -15.60),
    "Fuerteventura": (28.35, -14.00),
    "Lanzarote": (29.05, -13.60),
    "La Graciosa": (29.25, -13.50),
}

REQUIRED_COLUMNS = {
    "event_id",
    "occurred_at",
    "latitude",
    "longitude",
    "magnitude",
    "location",
    "source_url",
}


def island_for(latitude: float, longitude: float) -> str:
    """Classify a coordinate using its nearest Canary Island centre."""
    return min(
        ISLAND_CENTERS,
        key=lambda island: (
            (latitude - ISLAND_CENTERS[island][0]) ** 2
            + (longitude - ISLAND_CENTERS[island][1]) ** 2
        ),
    )


def load_events(path: Path = SAMPLE_DATA) -> pd.DataFrame:
    """Load and validate the public IGN CSV snapshot."""
    events = pd.read_csv(path, sep=";")
    missing = REQUIRED_COLUMNS.difference(events.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

    events["occurred_at"] = pd.to_datetime(events["occurred_at"], errors="raise")
    events["island"] = [
        island_for(latitude, longitude)
        for latitude, longitude in zip(
            events["latitude"],
            events["longitude"],
            strict=True,
        )
    ]
    return events.sort_values("occurred_at", ascending=False).reset_index(drop=True)


def filter_events(events: pd.DataFrame, selected_island: str) -> pd.DataFrame:
    """Return every event or a copy limited to one classified island."""
    if selected_island == "all":
        return events
    return events.loc[events["island"] == selected_island].reset_index(drop=True)
