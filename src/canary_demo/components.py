from __future__ import annotations

import pandas as pd
from dash import dcc, html

from canary_demo.data import ISLAND_CENTERS


def metric_card(label: str, value_id: str) -> html.Div:
    return html.Div(
        [html.Span(label), html.Strong(id=value_id)],
        className="metric-card",
    )


def event_cards(events: pd.DataFrame, selected_island: str) -> list:
    cards = [
        html.A(
            [
                html.Div(
                    [
                        html.Strong(f"M {event.magnitude:.1f}"),
                        html.Time(event.occurred_at.strftime("%d.%m.%Y · %H:%M")),
                    ]
                ),
                html.P(event.location),
                html.Small(
                    f"{event.island} · {event.latitude:.3f}, {event.longitude:.3f}"
                ),
            ],
            href=event.source_url,
            target="_blank",
            className="event-card",
        )
        for event in events.head(8).itertuples()
    ]
    if cards:
        return cards

    label = selected_island if selected_island != "all" else "the Canary Islands"
    return [
        html.Div(
            [
                html.Strong("No recorded events"),
                html.P(f"The public IGN snapshot contains no events for {label}."),
                html.Small("The dashboard is working correctly. Try another island."),
            ],
            className="empty",
        )
    ]


def dashboard_layout(events: pd.DataFrame) -> html.Main:
    snapshot = events["occurred_at"].max().strftime("%d %b %Y")

    return html.Main(
        [
            html.Header(
                [
                    html.Div(
                        [
                            html.Span(className="status-dot"),
                            "IGN DATA SNAPSHOT · PUBLIC DEMO",
                        ],
                        className="eyebrow",
                    ),
                    html.H1("Canary Seismic Monitor"),
                    html.P(
                        "Explore a curated snapshot of official Canary Islands "
                        f"seismic data · {snapshot}."
                    ),
                ]
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.Label("Filter by island"),
                            dcc.Dropdown(
                                id="island-filter",
                                options=[{"label": "All islands", "value": "all"}]
                                + [
                                    {"label": island, "value": island}
                                    for island in ISLAND_CENTERS
                                ],
                                value="all",
                                clearable=False,
                                searchable=False,
                            ),
                        ]
                    )
                ],
                className="filter-bar",
            ),
            html.Section(
                [
                    metric_card("Recorded events", "total"),
                    metric_card("Strongest magnitude", "strongest"),
                    metric_card("Latest event", "latest"),
                ],
                className="metrics",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.H2("Activity map"),
                            dcc.Graph(id="map", config={"displayModeBar": False}),
                        ],
                        className="map-panel",
                    ),
                    html.Div(
                        [
                            html.H2("Latest events"),
                            html.Div(id="event-list", className="event-list"),
                        ],
                        className="events-panel",
                    ),
                ],
                className="dashboard-grid",
            ),
            html.Section(
                [
                    html.Div(
                        [
                            html.H2("Activity history"),
                            html.P(
                                "Daily event count and strongest recorded magnitude",
                                className="section-note",
                            ),
                            dcc.Graph(
                                id="history",
                                config={"displayModeBar": False},
                            ),
                        ]
                    )
                ],
                className="history-panel",
            ),
            html.Footer(
                "Official data sample: Instituto Geografico Nacional (Spain) "
                "· Python · Dash · Plotly"
            ),
        ],
        className="page",
    )
