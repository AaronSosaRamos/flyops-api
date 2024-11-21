from crewai import Crew
from textwrap import dedent

from app.api.features.researcher.agents import FlyOpsResearcherAgents
from app.api.features.researcher.tasks import FlyOpsResearcherTasks
from app.api.schemas.flyops_researcher import (
    FlightResearchReport, 
    ResearchRequest
)

from langchain_core.output_parsers import JsonOutputParser

json_parser = JsonOutputParser(pydantic_object=FlightResearchReport)

class FlyOpsResearcherCrew:
    def __init__(self, date_range_start, date_range_end, focus_area, data_sources):
        self.research_request = ResearchRequest(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            focus_area=focus_area,
            data_sources=data_sources
        )
        self.agents = FlyOpsResearcherAgents()
        self.tasks = FlyOpsResearcherTasks()

    def run(self):
        # Define agents
        flight_data_analyst_agent = self.agents.flight_data_analyst_agent()
        trend_analyst_agent = self.agents.trend_analyst_agent()
        innovation_specialist_agent = self.agents.innovation_specialist_agent()
        research_report_generator_agent = self.agents.research_report_generator_agent()

        # Define tasks with the research request
        flight_data_analysis_task = self.tasks.flight_data_analysis_task(flight_data_analyst_agent, self.research_request)
        trend_analysis_task = self.tasks.trend_analysis_task(trend_analyst_agent, self.research_request)
        innovation_identification_task = self.tasks.innovation_identification_task(innovation_specialist_agent, self.research_request)
        research_report_task = self.tasks.research_report_task(research_report_generator_agent, self.research_request)

        # Create the crew
        crew = Crew(
            agents=[
                flight_data_analyst_agent,
                trend_analyst_agent,
                innovation_specialist_agent,
                research_report_generator_agent,
            ],
            tasks=[
                flight_data_analysis_task,
                trend_analysis_task,
                innovation_identification_task,
                research_report_task,
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return json_parser.parse(result.raw)