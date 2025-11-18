"""Router exports for centralized registration."""
from plantos_backend.routers.ai import router as ai_router
from plantos_backend.routers.experiments import router as experiments_router
from plantos_backend.routers.marketplace import router as marketplace_router
from plantos_backend.routers.meta import router as meta_router
from plantos_backend.routers.plants import router as plants_router
from plantos_backend.routers.propagation import router as propagation_router
from plantos_backend.routers.schedules import router as schedules_router

ALL_ROUTERS = [
    meta_router,
    plants_router,
    schedules_router,
    ai_router,
    experiments_router,
    propagation_router,
    marketplace_router,
]

__all__ = ["ALL_ROUTERS"]
