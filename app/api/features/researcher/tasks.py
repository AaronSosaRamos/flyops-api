from crewai import Task
from textwrap import dedent

from app.api.schemas.flyops_researcher import (
    FlightResearchReport, 
    ResearchRequest
)

class FlyOpsResearcherTasks:
    def __init__(self):
        pass

    def flight_data_analysis_task(self, agent, research_request: ResearchRequest):
        return Task(
            description=dedent(f"""
                Analyze flight operation data from **{research_request.date_range_start}** to **{research_request.date_range_end}** focusing on **{research_request.focus_area}**.
                Use the specified data sources: {', '.join(research_request.data_sources)}.
                Identify significant trends, patterns, and anomalies.
                Document each insight with detailed descriptions, supporting data points, and analysis methods used.
                **Use the provided tools to gather accurate and up-to-date information.**
            """),
            agent=agent,
            expected_output="A list of FlightDataInsight objects with detailed information as per the FlightDataInsight schema.",
        )

    def trend_analysis_task(self, agent, research_request: ResearchRequest):
        return Task(
            description=dedent(f"""
                Interpret the analyzed flight data related to **{research_request.focus_area}** to predict future trends in the aviation industry.
                Provide detailed explanations for each predicted trend, including possible implications and recommendations.
                **Use the provided tools to enhance your analysis.**
            """),
            agent=agent,
            expected_output="A set of future trends with detailed explanations and justifications.",
        )

    def innovation_identification_task(self, agent, research_request: ResearchRequest):
        return Task(
            description=dedent(f"""
                Identify recent innovations in flight data and technology within the area of **{research_request.focus_area}** that have the potential to revolutionize the aviation industry.
                Assess the impact of each innovation, backing your findings with data and references.
                **Use the provided tools to support your analysis.**
            """),
            agent=agent,
            expected_output="A list of FlightInnovation objects with detailed information as per the FlightInnovation schema.",
        )

    def research_report_task(self, agent, research_request: ResearchRequest):
        flight_research_report_schema = FlightResearchReport.schema_json(indent=2)
        return Task(
            description=dedent(f"""
                Compile a comprehensive research report based on the analyzed data and identified innovations for **{research_request.focus_area}** from **{research_request.date_range_start}** to **{research_request.date_range_end}**.
                Include the following in your report:
                - **Insights**: A detailed list of discovered insights, following the FlightDataInsight schema.
                - **Innovations**: A detailed list of identified innovations, following the FlightInnovation schema.
                - **Overall Analysis**: An in-depth analysis of the current and future state of flight operations related to **{research_request.focus_area}**.
                - **Future Trends**: Predictions about future developments in the aviation industry concerning **{research_request.focus_area}**.
                - **Recommendations**: Actionable recommendations based on your findings.
                - **Data Sources**: Include the data sources used: {', '.join(research_request.data_sources)}.
                - **Additional Notes**, **References**, **Contact Information**, **Legal Disclaimer**: Provide any additional relevant information.

                Provide your output in **JSON format** matching the **FlightResearchReport** schema below.

                **FlightResearchReport Schema**:

                {flight_research_report_schema}
            """),
            agent=agent,
            expected_output=f"The research report in JSON format matching the FlightResearchReport schema: {flight_research_report_schema}",
        )
