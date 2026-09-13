from canary_demo.data import filter_events, load_events
from canary_demo.figures import build_activity_map, build_history_chart


def test_activity_map_contains_highlight_and_event_layers() -> None:
    figure = build_activity_map(load_events(), "all")
    assert len(figure.data) == 2


def test_history_contains_count_and_magnitude_series() -> None:
    figure = build_history_chart(load_events())
    assert [trace.name for trace in figure.data] == [
        "Events",
        "Strongest magnitude",
    ]


def test_empty_island_figures_show_messages_without_empty_traces() -> None:
    events = filter_events(load_events(), "El Hierro")
    activity_map = build_activity_map(events, "El Hierro")
    history = build_history_chart(events)

    assert len(activity_map.data) == 0
    assert "El Hierro" in activity_map.layout.annotations[0].text
    assert len(history.data) == 0
    assert "No historical data" in history.layout.annotations[0].text
