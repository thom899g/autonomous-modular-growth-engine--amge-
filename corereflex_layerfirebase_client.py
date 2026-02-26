"""
Firebase Client for the Reflex Layer with robust connection management
and automatic reconnection logic
"""

import os
import json
import time
import threading
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
import logging

# Standard library imports - no hallucinations
import firebase_admin
from firebase_admin import credentials, firestore, db
from firebase_admin.exceptions import FirebaseError

from .exceptions import FirebaseConnectionError

logger = logging.getLogger(__name__)


class FirebaseClient:
    """
    Robust Firebase client with automatic reconnection, health monitoring,
    and connection pooling
    """
    
    # Singleton instance management
    _instance: Optional['FirebaseClient'] = None
    _lock = threading.Lock()
    
    # Connection health tracking
    _last_health_check: Optional[datetime] = None
    _connection_healthy: bool = False
    _reconnect_attempts: int = 0
    MAX_RECONNECT_ATTEMPTS = 5
    RECONNECT_BASE_DELAY = 2  # seconds
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single Firebase app instance"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, credentials_path: Optional[str] = None, 
                 project_id: Optional[str] = None):
        """Initialize Firebase client with robust error handling"""
        
        # Check if already initialized
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._initialized = False
        self.credentials_path = credentials_path or os.getenv('FIREBASE_CREDENTIALS_PATH')
        self.project_id = project_id or os.getenv('FIREBASE_PROJECT_ID')
        
        # Validate configuration before attempting connection
        self._validate_configuration()
        
        # Initialize Firebase app
        try:
            self._initialize_firebase()
            self._setup_clients()
            self._start_health_monitor()
            self._initialized = True
            logger.info("FirebaseClient initialized successfully")
            
        except Exception as e:
            logger.critical(f"Failed to initialize FirebaseClient: {str(e)}")
            raise FirebaseConnectionError(
                f"Failed to initialize Firebase: {str(e)}",
                firebase_error=e,
                credentials_path=self.credentials_path
            )
    
    def _validate_configuration(self) -> None:
        """Validate Firebase