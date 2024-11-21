from pydantic import BaseModel
from typing import List, Dict, Any

class ResearchRequest(BaseModel):
    date_range_start: str  # Format: 'YYYY-MM-DD'
    date_range_end: str    # Format: 'YYYY-MM-DD'
    focus_area: str        # Specific area of interest
    data_sources: List[str]

class FlightDataInsight(BaseModel):
    trend_name: str
    description: str
    data_points: List[Dict[str, Any]]  # Details of data points supporting the insight
    analysis_method: str
    implications: str
    recommendations: List[str]

class FlightInnovation(BaseModel):
    innovation_name: str
    description: str
    impact: str
    supporting_data: List[Dict[str, Any]]
    references: List[str]

class FlightResearchReport(BaseModel):
    insights: List[FlightDataInsight]
    innovations: List[FlightInnovation]
    overall_analysis: str
    future_trends: List[str]
    recommendations: List[str]
    data_sources: List[str]
    additional_notes: str
    references: List[str]
    contact_information: str
    legal_disclaimer: str
