from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from canary_demo.data import ISLAND_CENTERS


def _empty_message(figure: go.Figure, message: str) -> None:
    figure.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"color": "#96a3b6", "size": 15},
        bgcolor="rgba(12,19,32,0.88)",
        bordercolor="#344258",
        borderpad=12,
    )


def build_activity_map(
    events: pd.DataFrame,
    selected_island: str,
) -> go.Figure:
    """Create the interactive map and highlight the newest event."""
    figure = go.Figure()

    if not events.empty:
        newest = events.iloc[0]
        figure.add_trace(
            go.Scattermap(
                lat=[newest["latitude"]],
                lon=[newest["longitude"]],
                mode="markers",
                marker={
                    "size": 38,
                    "color": "rgba(255,92,69,0.24)",
                },
                hoverinfo="skip",
                showlegend=False,
            )
        )
        figure.add_trace(
            go.Scattermap(
                lat=events["latitude"],
                lon=events["longitude"],
                mode="markers",
                customdata=events[
                    ["location", "occurred_at", "magnitude", "island"]
                ].to_numpy(),
                marker={
                    "size": (12 + events["magnitude"] * 6).tolist(),
                    "color": events["magnitude"],
                    "colorscale": "YlOrRd",
                    "showscale": True,
                    "colorbar": {"title": {"text": "M"}},
                },
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "%{customdata[3]} · M %{customdata[2]}<br>"
                    "%{customdata[1]|%d.%m.%Y %H:%M}<extra></extra>"
                ),
            )
        )
    else:
        label = selected_island if selected_island != "all" else "the Canary Islands"
        _empty_message(figure, f"No recorded events for {label}")

    center = ISLAND_CENTERS.get(selected_island, (28.3, -16.0))
    figure.update_layout(
        map={
            "style": "open-street-map",
            "center": {"lat": center[0], "lon": center[1]},
            "zoom": 8 if selected_island != "all" else 5.7,
        },
        uirevision=selected_island,
        paper_bgcolor="#111827",
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        showlegend=False,
    )
    return figure


def build_history_chart(events: pd.DataFrame) -> go.Figure:
    """Create daily event-count and strongest-magnitude series."""
    figure = go.Figure()
    if not events.empty:
        daily = (
            events.assign(day=events["occurred_at"].dt.strftime("%d.%m"))
            .groupby("day", sort=False)["magnitude"]
            .agg(event_count="size", strongest="max")
            .iloc[::-1]
        )
        figure.add_bar(
            x=daily.index,
            y=daily["event_count"],
            name="Events",
            marker_color="#ff775c",
        )
        figure.add_scatter(
            x=daily.index,
            y=daily["strongest"],
            name="Strongest magnitude",
            mode="lines+markers",
            yaxis="y2",
            line={"color": "#ffd166", "width": 3},
        )
    else:
        _empty_message(figure, "No historical data for the selected filter")

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 35, "r": 35, "t": 20, "b": 30},
        legend={"orientation": "h", "y": 1.12},
        yaxis={
            "title": "Events",
            "gridcolor": "#263040",
            "rangemode": "tozero",
            "dtick": 1,
        },
        yaxis2={
            "title": "Magnitude",
            "overlaying": "y",
            "side": "right",
            "rangemode": "tozero",
        },
    )
    return figure
