"""
Autonomous Modular Growth Engine - Reflex Layer
Firebase-backed Event Mesh for real-time reactive processing
Version: 1.0.0
"""

from .firebase_client import FirebaseClient
from .event_mesh import EventMesh
from .materialized_views import MaterializedViewManager
from .exceptions import (
    FirebaseConnectionError,
    EventValidationError,
    MaterializedViewError,
    ReflexLayerError
)

__version__ = "1.0.0"
__all__ = [
    "FirebaseClient",
    "EventMesh",
    "MaterializedViewManager",
    "FirebaseConnectionError",
    "EventValidationError",
    "MaterializedViewError",
    "ReflexLayerError"
]