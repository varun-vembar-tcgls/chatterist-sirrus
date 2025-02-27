from typing import Optional
from fastapi import Depends, HTTPException
from app.utils.gemini_integration import GeminiService
from app.config import Settings, get_settings

# Global instance for the Gemini service to avoid reinitializing
_gemini_service = None

def extract_auth_token(authorization: Optional[str] = None) -> Optional[str]:
    """
    Extract the token from the Authorization header if provided
    """
    if authorization and authorization.startswith("Bearer "):
        return authorization.split("Bearer ")[1]
    return None

def get_gemini_service(settings: Settings = Depends(get_settings)) -> GeminiService:
    """
    Get or initialize the Gemini service
    """
    global _gemini_service
    
    if _gemini_service is None:
        if not settings.gemini_api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured")
        _gemini_service = GeminiService(api_key=settings.gemini_api_key)
    
    return _gemini_service