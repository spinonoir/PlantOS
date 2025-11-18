"""CLI entrypoint for running the FastAPI app with uvicorn."""
from __future__ import annotations

import uvicorn

from plantos_backend.settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "plantos_backend.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        factory=False,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
