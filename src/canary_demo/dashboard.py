from __future__ import annotations

from pathlib import Path

from dash import Dash, Input, Output

from canary_demo.components import dashboard_layout, event_cards
from canary_demo.data import SAMPLE_DATA, filter_events, load_events
from canary_demo.figures import build_activity_map, build_history_chart


ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"


def create_app(data_path: Path = SAMPLE_DATA) -> Dash:
    """Create the Dash application around a reproducible IGN snapshot."""
    all_events = load_events(data_path)
    app = Dash(
        __name__,
        title="Canary Seismic Monitor — Demo",
        assets_folder=str(ASSETS_DIR),
    )
    app.layout = dashboard_layout(all_events)

    @app.callback(
        Output("total", "children"),
        Output("strongest", "children"),
        Output("latest", "children"),
        Output("map", "figure"),
        Output("event-list", "children"),
        Output("history", "figure"),
        Input("island-filter", "value"),
    )
    def refresh(selected_island: str):
        events = filter_events(all_events, selected_island)
        latest = (
            events.iloc[0]["occurred_at"].strftime("%d.%m · %H:%M")
            if not events.empty
            else "—"
        )
        strongest = f"M {events['magnitude'].max():.1f}" if not events.empty else "—"

        return (
            str(len(events)),
            strongest,
            latest,
            build_activity_map(events, selected_island),
            event_cards(events, selected_island),
            build_history_chart(events),
        )

    return app
