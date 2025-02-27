# api_client.py
import requests
from typing import Dict, Any, Optional
import logging

def get_project_leads(
    organisation_id: str, 
    project_id: str, 
    settings,
    auth_token: Optional[str] = None,
    client_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve all leads for a specific organisation and project.
    
    Args:
        organisation_id: The organisation identifier
        project_id: The project identifier
        settings: Application settings containing API configuration
        auth_token: Optional token to override settings.bearer_token
        client_id: Optional client_id to override settings.client_id
        
    Returns:
        Dict containing the leads data grouped by lead status
    """
    url = f"{settings.api_base_url}/organisations/{organisation_id}/projects/{project_id}/leads"
    
    # Query parameters
    params = {
        "groupBy": settings.group_by,
        "mapRelatedEntities": settings.map_related_entities,
        "limit": settings.limit
    }
    
    # Request headers with override capability
    headers = {
        'Authorization': f'Bearer {auth_token if auth_token else settings.bearer_token}',
        'client_id': client_id if client_id else settings.client_id
    }
    
    # Log the request details for debugging
    logging.info(f"Making request to URL: {url}")
    logging.info(f"Headers: {headers}")
    logging.info(f"Params: {params}")
    
    # Send the request
    response = requests.get(url, headers=headers, params=params)
    
    # Log the response for debugging
    logging.info(f"Response status code: {response.status_code}")
    
    # Handle non-200 responses with more details
    if response.status_code != 200:
        logging.error(f"Error response: {response.text}")
        response.raise_for_status()
    
    return response.json()