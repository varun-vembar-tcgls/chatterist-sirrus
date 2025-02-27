# app/utils/lead_functions.py
from typing import Dict, Any, List
from app.utils.api_client import get_project_leads
from app.utils.leads_processor import get_and_process_leads
from app.config import Settings

# Global variables to store context
_organisation_id = None
_project_id = None
_settings = None

def set_lead_context(organisation_id: str, project_id: str, settings: Settings):
    """Set the global context for lead functions"""
    global _organisation_id, _project_id, _settings
    _organisation_id = organisation_id
    _project_id = project_id
    _settings = settings

def get_leads():
    """Get all leads for the organization and project"""
    leads_data = get_project_leads(
        organisation_id=_organisation_id,
        project_id=_project_id,
        settings=_settings
    )
    processed = get_and_process_leads(
        organisation_id=_organisation_id,
        project_id=_project_id,
        settings=_settings
    )
    return {
        "total_leads": processed.get("total_leads", 0),
        "lead_status_summary": processed.get("lead_status_summary", {}),
        "lead_sources": processed.get("lead_sources", {})
    }

def get_lead_by_status(status: str):
    """Get leads filtered by status"""
    processed = get_and_process_leads(
        organisation_id=_organisation_id,
        project_id=_project_id,
        settings=_settings
    )
    
    matching_leads = [
        lead for lead in processed.get("leads", [])
        if lead.get("status", "").lower() == status.lower()
    ]
    
    return {
        "status": status,
        "count": len(matching_leads),
        "leads": matching_leads 
    }

def get_lead_by_source(source: str):
    """Get leads filtered by source"""
    processed = get_and_process_leads(
        organisation_id=_organisation_id,
        project_id=_project_id,
        settings=_settings
    )
    
    matching_leads = [
        lead for lead in processed.get("leads", [])
        if lead.get("sourceOfLead", "").lower() == source.lower()
    ]
    
    return {
        "source": source,
        "count": len(matching_leads),
        "leads": matching_leads
    }

def get_lead_stats():
    """Get statistical summary of leads"""
    processed = get_and_process_leads(
        organisation_id=_organisation_id,
        project_id=_project_id,
        settings=_settings
    )
    
    return {
        "total_leads": processed.get("total_leads", 0),
        "by_status": processed.get("lead_status_summary", {}),
        "by_source": processed.get("lead_sources", {}),
        "by_assignee": processed.get("leads_by_assignee", {})
    }