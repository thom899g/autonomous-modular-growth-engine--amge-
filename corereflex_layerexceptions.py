"""
Custom exceptions for the Reflex Layer with comprehensive error handling
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ReflexLayerError(Exception):
    """Base exception for all Reflex Layer errors"""
    def __init__(self, message: str, component: str = "unknown", 
                 context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.component = component
        self.context = context or {}
        super().__init__(f"[{component}] {message}")
        logger.error(f"ReflexLayerError in {component}: {message}", 
                    extra={"context": context})


class FirebaseConnectionError(ReflexLayerError):
    """Raised when Firebase connection fails"""
    def __init__(self, message: str, firebase_error: Optional[Exception] = None,
                 credentials_path: Optional[str] = None):
        context = {
            "firebase_error": str(firebase_error) if firebase_error else None,
            "credentials_path": credentials_path
        }
        super().__init__(message, "firebase_client", context)


class EventValidationError(ReflexLayerError):
    """Raised when event validation fails"""
    def __init__(self, message: str, event_data: Dict[str, Any], 
                 validation_rules: Optional[Dict] = None):
        context = {
            "event_data": event_data,
            "validation_rules": validation_rules,
            "schema_violations": self._extract_schema_violations(event_data, validation_rules)
        }
        super().__init__(message, "event_mesh", context)
    
    @staticmethod
    def _extract_schema_violations(event_data: Dict, rules: Optional[Dict]) -> Dict:
        """Extract specific schema violations for better debugging"""
        violations = {}
        if not rules:
            return violations
        
        required_fields = rules.get("required_fields", [])
        for field in required_fields:
            if field not in event_data:
                violations[field] = "Missing required field"
        
        return violations


class MaterializedViewError(ReflexLayerError):
    """Raised when materialized view operations fail"""
    def __init__(self, message: str, view_name: str, 
                 operation: str, data: Optional[Dict] = None):
        context = {
            "view_name": view_name,
            "operation": operation,
            "data_size": len(data) if data else 0
        }
        super().__init__(message, "materialized_views", context)