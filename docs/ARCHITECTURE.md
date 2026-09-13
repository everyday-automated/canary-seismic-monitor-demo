# Public Demo Architecture

The public demo is a small layered Dash application built around a deterministic snapshot of official IGN earthquake data.

![Architecture diagram](images/architecture.svg)

## Design goals

- keep the public example fully runnable;
- make every transformation easy to inspect and test;
- separate data, presentation and orchestration concerns;
- preserve a clear boundary between the portfolio demo and private production automation.

## Modules

### `app.py`

The process entry point. It creates the Dash application, exposes its Flask server and binds to the port supplied by the environment.

### `canary_demo.data`

Owns the input contract and deterministic transformations:

- validates the CSV schema;
- parses event timestamps;
- classifies coordinates by their nearest Canary Island centre;
- orders events newest-first;
- applies the selected island filter.

### `canary_demo.figures`

Builds Plotly figures without knowing anything about the web layout:

- an interactive activity map;
- a static highlight layer for the newest event;
- a daily event-count series;
- a strongest-magnitude series.

### `canary_demo.components`

Defines reusable Dash presentation components, including metric cards, event cards and the responsive page layout.

### `canary_demo.dashboard`

Composes the modules into an application and owns the callback that converts UI state into metrics, cards and figures.

## Runtime sequence

1. Dash starts and loads the bundled CSV snapshot.
2. The data layer validates and enriches the events with an island classification.
3. The layout renders the filter, metrics and visualization containers.
4. A user changes the island filter.
5. The callback selects the relevant events.
6. The figure layer produces the map and historical chart.
7. Dash sends the updated component tree to the browser.

## CSV contract

| Field | Purpose |
| --- | --- |
| `event_id` | Stable IGN event identifier |
| `occurred_at` | ISO timestamp of the event |
| `latitude` | Epicentre latitude |
| `longitude` | Epicentre longitude |
| `magnitude` | Reported magnitude |
| `location` | IGN location label |
| `source_url` | Official source reference |

The derived `island` field is calculated at load time and is not stored in the original snapshot.

## Public/private boundary

The public demo intentionally contains no HTTP ingestion client, scheduler, filesystem observer or persistent storage. Those components belong to the private production repository.

This is a product boundary rather than a mocked implementation: the public visualization and transformation code is real, while the operational ingestion pipeline remains private.
