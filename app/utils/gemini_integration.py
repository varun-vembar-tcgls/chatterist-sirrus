import google.generativeai as genai
import json
from typing import Dict, Any, List

class GeminiService:
    """
    Service for integrating Gemini AI to answer questions about leads data.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
    def analyze_leads(self, leads_data: Dict[str, Any], query: str) -> str:
        """
        Analyze leads data and answer a query about it using Gemini.
        
        Args:
            leads_data: The leads data retrieved from the API
            query: The user's question about the leads data
            
        Returns:
            str: Gemini's response to the query
        """
        # Prepare context for Gemini with important information from leads data
        context = self._prepare_context(leads_data)
        
        # Combine context and query for Gemini
        prompt = f"""
        As an AI assistant with access to leads data from a CRM system, please answer the following question 
        based solely on the data provided below:
        
        --- LEADS DATA ---
        {context}
        
        --- USER QUERY ---
        {query}
        
        Only use the information from the provided data to answer. If the data doesn't contain information to 
        answer the query, say so clearly. Provide specific details when available.
        """
        
        # Get response from Gemini
        response = self.model.generate_content(prompt)
        return response.text
    
    def _prepare_context(self, leads_data: Dict[str, Any]) -> str:
        """
        Extract and format the most relevant information from leads data to provide as context.
        
        Args:
            leads_data: The complete leads data from API
            
        Returns:
            str: Formatted context with key information
        """
        if not leads_data or 'data' not in leads_data:
            return "No leads data available."
        
        # Extract lead statuses and their counts
        lead_status_summary = {}
        all_leads = []
        
        # Process each lead status group
        for status_group in leads_data.get('data', {}).get('items', []):
            status_name = status_group.get('leadStatus', 'Unknown')
            items = status_group.get('items', [])
            lead_count = len(items)
            
            # Get the actual status label
            status_label = "Unknown"
            if items and 'leadStatus' in items[0] and 'labelName' in items[0]['leadStatus']:
                status_label = items[0]['leadStatus']['labelName']
            
            lead_status_summary[status_label] = lead_count
            
            # Extract key info from each lead
            for lead in items:
                lead_info = {
                    "leadId": lead.get('leadId', 'Unknown'),
                    "status": status_label,
                    "fullName": lead.get('profile', {}).get('fullName', 'Unknown'),
                    "sourceOfLead": lead.get('profile', {}).get('sourceOfLead', {}).get('labelName', 'Unknown'),
                    "subSourceOfLead": lead.get('profile', {}).get('subSourceOfLead', {}).get('labelName', 'Unknown'),
                    "assignee": f"{lead.get('assigneeId', {}).get('firstName', '')} {lead.get('assigneeId', {}).get('lastName', '')}".strip(),
                    "createdAt": lead.get('createdAt', 'Unknown'),
                    "updatedAt": lead.get('updatedAt', 'Unknown'),
                    "conversionPropensity": lead.get('conversionPropensity', {}).get('probability', 'Unknown') if 'conversionPropensity' in lead else 'Unknown'
                }
                all_leads.append(lead_info)
        
        # Format the context
        context = f"Lead Status Summary: {json.dumps(lead_status_summary, indent=2)}\n\n"
        context += f"Total Leads: {len(all_leads)}\n\n"
        context += "Lead Details:\n"
        
        for i, lead in enumerate(all_leads):
            context += f"Lead {i+1}:\n"
            for key, value in lead.items():
                context += f"  {key}: {value}\n"
            context += "\n"
            
        return context