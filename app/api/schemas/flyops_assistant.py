from pydantic import BaseModel

class FlyOpsAssistantInput(BaseModel):
    query: str