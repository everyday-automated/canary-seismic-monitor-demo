import os

from canary_demo.dashboard import create_app


app = create_app()
server = app.server


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8050")),
        debug=False,
    )
