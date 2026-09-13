from canary_demo.dashboard import create_app


def test_dashboard_has_expected_title_and_callbacks() -> None:
    app = create_app()
    assert app.title == "Canary Seismic Monitor — Demo"
    assert len(app.callback_map) == 1
    callback_config = next(iter(app.callback_map.values()))
    assert callback_config["inputs"] == [
        {"id": "island-filter", "property": "value"}
    ]

    callback = callback_config["callback"].__wrapped__
    total, strongest, latest, activity_map, cards, history = callback("El Hierro")
    assert (total, strongest, latest) == ("0", "—", "—")
    assert len(activity_map.data) == 0
    assert cards[0].children[0].children == "No recorded events"
    assert len(history.data) == 0
