from fastapi import FastAPI, Depends, HTTPException, Body
import uvicorn
from typing import Dict, Any
from pydantic import BaseModel
from app.utils.api_client import get_project_leads
from app.utils.leads_processor import get_and_process_leads
from app.utils.gemini_integration import GeminiService
from app.config import Settings, get_settings

app = FastAPI(title="Leads API Service")

# Initialize gemini service
gemini_service = None

# Pydantic models
class QueryRequest(BaseModel):
    query: str

@app.get("/api/leads/{organisation_id}/{project_id}")
async def fetch_leads(
    organisation_id: str,
    project_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    Fetch all leads for a specific organisation and project.
    
    Parameters:
    - organisation_id: The organisation identifier
    - project_id: The project identifier
    
    Returns:
    - JSON response containing lead data grouped by lead status
    """
    try:
        leads_data = get_project_leads(organisation_id, project_id, settings)
        return leads_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/processed-leads/{organisation_id}/{project_id}")
async def fetch_processed_leads(
    organisation_id: str,
    project_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    Fetch and process leads data for a specific organisation and project.
    
    Parameters:
    - organisation_id: The organisation identifier
    - project_id: The project identifier
    
    Returns:
    - Processed lead data with summaries and structured information
    """
    try:
        processed_data = get_and_process_leads(organisation_id, project_id, settings)
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/query-leads/{organisation_id}/{project_id}")
async def query_leads_with_ai(
    organisation_id: str,
    project_id: str,
    request: QueryRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Query leads data using Gemini AI to get insights and answers to natural language questions.
    
    Parameters:
    - organisation_id: The organisation identifier
    - project_id: The project identifier
    - request: The query request containing the natural language question
    
    Returns:
    - AI-generated response to the query based on leads data
    """
    global gemini_service
    
    try:
        # Initialize Gemini service if not already done
        if gemini_service is None:
            if not settings.gemini_api_key:
                raise HTTPException(status_code=500, detail="Gemini API key not configured")
            gemini_service = GeminiService(api_key=settings.gemini_api_key)
        
        # Get raw leads data from the API
        leads_data = get_project_leads(organisation_id, project_id, settings)
        
        # Process the query with Gemini AI
        response = gemini_service.analyze_leads(leads_data, request.query)
        
        return {
            "query": request.query,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)