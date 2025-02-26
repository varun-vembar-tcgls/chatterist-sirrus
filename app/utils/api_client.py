# api_client.py
import requests
from typing import Dict, Any

def get_project_leads(organisation_id: str, project_id: str, settings) -> Dict[str, Any]:
    """
    Retrieve all leads for a specific organisation and project.
    
    Args:
        organisation_id: The organisation identifier
        project_id: The project identifier
        settings: Application settings containing API configuration
        
    Returns:
        Dict containing the leads data grouped by lead status
    """
    url = f"{settings.api_base_url}/organisations/{organisation_id}/projects/{project_id}/leads"
    
    # Query parameters 
    params = {
        "groupBy": "leadStatus",
        "mapRelatedEntities": "true",
        "limit": "9999999999"
    }
    
    # Request headers - exactly matching the curl command
    headers = {
        'Authorization': f'Bearer {settings.bearer_token}',
        'client_id': 'TCG-WEB-APP'
    }
    
    # Send the request
    response = requests.get(url, headers=headers, params=params)
    
    # Raise an exception for bad status codes
    response.raise_for_status()
    
    return response.json()