from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from app.utils.api_client import get_project_leads
from app.utils.gemini_integration import GeminiService
from app.utils.lead_functions import set_lead_context, get_leads, get_lead_by_status, get_lead_by_source, get_lead_stats
from app.config import Settings, get_settings
from app.dependencies import extract_auth_token, get_gemini_service

router = APIRouter(prefix="/api/ai", tags=["ai"])

class ChatRequest(BaseModel):
    message: str
    
    @staticmethod
    def get_system_prompt():
        """Read system prompt from text file"""
        with open('app/prompts/lead_system_prompt.txt', 'r') as file:
            return file.read()

@router.post("/chat-with-leads/{organisation_id}/{project_id}")
async def chat_with_leads(
    organisation_id: str,
    project_id: str,
    request: ChatRequest,
    authorization: Optional[str] = Header(None),
    client_id: Optional[str] = Header(None),
    gemini_service: GeminiService = Depends(get_gemini_service),
    settings: Settings = Depends(get_settings)
):
    """
    Chat with Gemini AI about leads data with function calling capabilities.
    """
    try:
        # Extract token if provided
        auth_token = extract_auth_token(authorization)
        
        # Set up the context for lead functions
        set_lead_context(
            organisation_id=organisation_id,
            project_id=project_id,
            settings=settings
        )
        
        # Get system prompt from the class method
        system_prompt = ChatRequest.get_system_prompt()
        
        # List of tool functions
        tools = [get_leads, get_lead_by_status, get_lead_by_source, get_lead_stats]
        
        # Create a model with function calling
        chat = gemini_service.create_function_calling_model(
            tools=tools,
            system_instruction=system_prompt
        )
        
        # Send the message and get the response
        response = chat.send_message(request.message)
        
        return {
            "message": request.message,
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))