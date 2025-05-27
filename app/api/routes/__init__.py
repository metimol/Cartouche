"""
API routes initialization for the Cartouche Bot Service.
"""

from fastapi import APIRouter

from app.api.routes import bots, monitoring

# Create router
router = APIRouter()

# Include sub-routers
router.include_router(bots.router, prefix="/bots", tags=["bots"])
router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
