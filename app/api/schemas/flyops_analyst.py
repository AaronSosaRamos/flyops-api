from pydantic import BaseModel
from typing import List, Dict, Any

class FlightRequest(BaseModel):
    origin: str
    destination: str
    date: str  # Format: 'YYYY-MM-DD'
    available_budget: float

class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure_time: str  # Format: 'YYYY-MM-DD HH:MM'
    arrival_time: str    # Format: 'YYYY-MM-DD HH:MM'
    duration: str        # Format: 'HH:MM'
    price: float
    stops: int
    layover_cities: List[str]
    aircraft_type: str
    seat_class: str
    amenities: List[str]
    booking_link: str

class FlightAnalysis(BaseModel):
    recommended_flights: List[FlightOption]
    total_cost_savings: float
    cost_breakdown: Dict[str, float]  # Mapping flight numbers to cost
    alternative_routes: List[FlightOption]
    analysis_details: Dict[str, Any]  # Details about analysis criteria and methods
    recommendations: List[str]
    potential_challenges: List[str]
    additional_notes: str
    resources: List[str]
    contact_information: str
    legal_disclaimer: str