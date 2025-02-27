# leads_processor.py
import json
from typing import Dict, Any, List, Optional
from .api_client import get_project_leads

def process_leads_data(leads_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and structure the leads data from the API response.
    
    Args:
        leads_data: Raw leads data from the API
        
    Returns:
        Processed and structured leads data
    """
    if not leads_data or 'data' not in leads_data:
        return {"error": "No leads data available"}
    
    result = {
        "total_leads": 0,
        "lead_status_summary": {},
        "lead_sources": {},
        "leads_by_assignee": {},
        "leads": []
    }
    
    # Process each lead status group
    for status_group in leads_data.get('data', {}).get('items', []):
        status_id = status_group.get('leadStatus', 'Unknown')
        items = status_group.get('items', [])
        
        # Get the actual status label 
        status_label = "Unknown"
        if items and 'leadStatus' in items[0] and 'labelName' in items[0]['leadStatus']:
            status_label = items[0]['leadStatus']['labelName']
        
        result['lead_status_summary'][status_label] = len(items)
        result['total_leads'] += len(items)
        
        # Process each lead
        for lead in items:
            # Extract source information
            source = lead.get('profile', {}).get('sourceOfLead', {}).get('labelName', 'Unknown')
            if source not in result['lead_sources']:
                result['lead_sources'][source] = 0
            result['lead_sources'][source] += 1
            
            # Extract assignee information
            assignee = f"{lead.get('assigneeId', {}).get('firstName', '')} {lead.get('assigneeId', {}).get('lastName', '')}".strip()
            if not assignee:
                assignee = "Unassigned"
            
            if assignee not in result['leads_by_assignee']:
                result['leads_by_assignee'][assignee] = 0
            result['leads_by_assignee'][assignee] += 1
            
            # Extract core lead information
            lead_info = {
                "leadId": lead.get('leadId', 'Unknown'),
                "status": status_label,
                "fullName": lead.get('profile', {}).get('fullName', 'Unknown'),
                "sourceOfLead": source,
                "subSourceOfLead": lead.get('profile', {}).get('subSourceOfLead', {}).get('labelName', 'Unknown'),
                "assignee": assignee,
                "createdAt": lead.get('createdAt', 'Unknown'),
                "updatedAt": lead.get('updatedAt', 'Unknown'),
                "conversionPropensity": lead.get('conversionPropensity', {}).get('probability', 'Unknown') if 'conversionPropensity' in lead else 'Unknown',
                "suggestiveAction": lead.get('suggestiveAction', 'Unknown')
            }
            
            result['leads'].append(lead_info)
    
    return result

def get_and_process_leads(
    organisation_id: str, 
    project_id: str, 
    settings,
    auth_token: Optional[str] = None,
    client_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve leads data from API and process it into a more usable format.
    
    Args:
        organisation_id: The organisation ID
        project_id: The project ID
        settings: Application settings
        auth_token: Optional token to override settings.bearer_token
        client_id: Optional client_id to override settings.client_id
        
    Returns:
        Processed leads data
    """
    try:
        # Get raw leads data from API
        raw_leads_data = get_project_leads(
            organisation_id=organisation_id, 
            project_id=project_id, 
            settings=settings,
            auth_token=auth_token,
            client_id=client_id
        )
        
        # Process the data
        processed_data = process_leads_data(raw_leads_data)
        
        return processed_data
    except Exception as e:
        return {"error": str(e)}