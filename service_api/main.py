from uvicorn import run

from service_api.bootstrap import make_app  # noqa


def main() -> None:
    run(
        app='service_api.main:make_app',
        host='0.0.0.0',
        port=8000,
        factory=True,
        workers=1,
    )
