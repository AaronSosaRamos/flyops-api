#from app.api.features.schemas.schemas import RequestSchema, SpellingCheckerRequestArgs
from fastapi import APIRouter, Depends
from app.api.features.analyst.crew import FlyOpsAnalystCrew
from app.api.features.assistant.assistant import generate_response_assistant
from app.api.features.assistant.db.db import create_database
from app.api.logger import setup_logger
from app.api.auth.auth import key_check
from app.api.schemas.flyops_analyst import FlightRequest
from app.api.schemas.flyops_assistant import FlyOpsAssistantInput

logger = setup_logger(__name__)
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/create-db")
async def create_database_resource( _ = Depends(key_check)):
    logger.info(f"Creating the database...")
    create_database()    
    logger.info("The database was successfully created")

    return True

@router.post("/flyops-assistant")
async def flyops_assistant(data: FlyOpsAssistantInput, _ = Depends(key_check)):
    logger.info(f"Generating the response...")
    result = generate_response_assistant(data.query)
    logger.info("The response was successfully created")
    return result

@router.post("/flyops-analyst")
async def flyops_analyst(data: FlightRequest, _ = Depends(key_check)):
    logger.info(f"Generating the response...")
    flyops_analyst = FlyOpsAnalystCrew(
        origin=data.origin,
        destination=data.origin,
        date=data.date,
        available_budget=data.available_budget
    )
    result = flyops_analyst.run()
    logger.info("The response was successfully created")
    return result