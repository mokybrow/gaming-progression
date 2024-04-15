from uvicorn import run

from gaming_progression_api.bootstrap import make_app  # noqa


def main() -> None:
    run(app='gaming_progression_api.main:make_app', host='127.0.0.1', port=8000, factory=True, workers=1, reload=True)
