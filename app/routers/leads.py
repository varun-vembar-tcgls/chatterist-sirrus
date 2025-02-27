from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import Dict, Any, Optional
from app.utils.api_client import get_project_leads
from app.utils.leads_processor import get_and_process_leads
from app.config import Settings, get_settings
from app.dependencies import extract_auth_token

router = APIRouter(prefix="/api", tags=["leads"])

@router.get("/leads")
async def fetch_leads_with_params(
    organisation_id: str = Query(..., description="The organisation identifier"),
    project_id: str = Query(..., description="The project identifier"),
    authorization: Optional[str] = Header(None, description="Bearer token for authorization"),
    client_id: Optional[str] = Header("TCG-WEB-APP", description="Client ID"),
    settings: Settings = Depends(get_settings)
):
    """
    Fetch all leads for a specific organisation and project with query parameters.
    """
    try:
        auth_token = extract_auth_token(authorization)
        leads_data = get_project_leads(
            organisation_id=organisation_id,
            project_id=project_id,
            settings=settings,
            auth_token=auth_token,
            client_id=client_id
        )
        return leads_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/{organisation_id}/{project_id}")
async def fetch_leads(
    organisation_id: str,
    project_id: str,
    authorization: Optional[str] = Header(None),
    client_id: Optional[str] = Header(None),
    settings: Settings = Depends(get_settings)
):
    """
    Fetch all leads for a specific organisation and project with path parameters.
    """
    try:
        auth_token = extract_auth_token(authorization)
        leads_data = get_project_leads(
            organisation_id=organisation_id,
            project_id=project_id,
            settings=settings,
            auth_token=auth_token,
            client_id=client_id
        )
        return leads_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processed-leads/{organisation_id}/{project_id}")
async def fetch_processed_leads(
    organisation_id: str,
    project_id: str,
    authorization: Optional[str] = Header(None),
    client_id: Optional[str] = Header(None),
    settings: Settings = Depends(get_settings)
):
    """
    Fetch and process leads data for a specific organisation and project.
    """
    try:
        auth_token = extract_auth_token(authorization)
        processed_data = get_and_process_leads(
            organisation_id=organisation_id,
            project_id=project_id,
            settings=settings,
            auth_token=auth_token,
            client_id=client_id
        )
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))