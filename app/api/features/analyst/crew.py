from crewai import Crew
from textwrap import dedent

from app.api.features.analyst.agents import FlyOpsAnalystAgents
from app.api.features.analyst.tasks import FlyOpsAnalystTasks
from app.api.schemas.flyops_analyst import FlightAnalysis, FlightRequest

from langchain_core.output_parsers import JsonOutputParser

json_parser = JsonOutputParser(pydantic_object=FlightAnalysis)

class FlyOpsAnalystCrew:
    def __init__(self, origin, destination, date, available_budget):
        self.flight_request = FlightRequest(
            origin=origin,
            destination=destination,
            date=date,
            available_budget=available_budget
        )
        self.agents = FlyOpsAnalystAgents()
        self.tasks = FlyOpsAnalystTasks()

    def run(self):
        # Define agents
        flight_data_collector_agent = self.agents.flight_data_collector_agent()
        flight_optimizer_agent = self.agents.flight_optimizer_agent()
        cost_analysis_agent = self.agents.cost_analysis_agent()
        report_generator_agent = self.agents.report_generator_agent()

        # Define tasks
        flight_data_collection_task = self.tasks.flight_data_collection_task(flight_data_collector_agent, self.flight_request)
        flight_optimization_task = self.tasks.flight_optimization_task(flight_optimizer_agent, self.flight_request)
        cost_analysis_task = self.tasks.cost_analysis_task(cost_analysis_agent, self.flight_request)
        flight_analysis_report_task = self.tasks.flight_analysis_report_task(report_generator_agent, self.flight_request)

        # Create the crew
        crew = Crew(
            agents=[
                flight_data_collector_agent,
                flight_optimizer_agent,
                cost_analysis_agent,
                report_generator_agent,
            ],
            tasks=[
                flight_data_collection_task,
                flight_optimization_task,
                cost_analysis_task,
                flight_analysis_report_task,
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return json_parser.parse(result.raw)