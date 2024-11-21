from crewai import Task
from textwrap import dedent

from app.api.schemas.flyops_analyst import FlightAnalysis, FlightRequest

class FlyOpsAnalystTasks:
    def __init__(self):
        pass

    def flight_data_collection_task(self, agent, flight_request: FlightRequest):
        return Task(
            description=dedent(f"""
                Collect all available flights from **{flight_request.origin}** to **{flight_request.destination}** on **{flight_request.date}** within the budget of **${flight_request.available_budget}**.
                Provide detailed flight options including all attributes defined in the FlightOption schema.
                **Use the tools provided to gather accurate and up-to-date flight information.**
            """),
            agent=agent,
            expected_output="A list of available flights that meet the user's criteria, with detailed information per the FlightOption schema.",
        )

    def flight_optimization_task(self, agent, flight_request: FlightRequest):
        return Task(
            description=dedent(f"""
                Analyze the collected flight options and recommend the best flights considering factors such as price, duration, number of stops, layover cities, aircraft type, seat class, and amenities.
                Provide detailed explanations for your recommendations, including potential cost savings and benefits.
                **Use the tools provided to enhance your analysis.**
            """),
            agent=agent,
            expected_output="A set of recommended flights with detailed explanations and justifications.",
        )

    def cost_analysis_task(self, agent, flight_request: FlightRequest):
        return Task(
            description=dedent(f"""
                Provide a detailed cost analysis for the user's flight from **{flight_request.origin}** to **{flight_request.destination}** on **{flight_request.date}**.
                Include a cost breakdown per flight option, total potential cost savings, and suggest alternative routes or options that could further reduce costs.
                **Use the tools provided to support your recommendations.**
            """),
            agent=agent,
            expected_output="Detailed cost analysis with cost breakdown, total savings, and alternative suggestions.",
        )

    def flight_analysis_report_task(self, agent, flight_request: FlightRequest):
        flight_analysis_schema = FlightAnalysis.schema_json(indent=2)
        return Task(
            description=dedent(f"""
                Compile a comprehensive flight analysis report based on the collected data and analyses.
                Include the following in your report:
                - **Recommended Flights**: A detailed list of recommended flights, including all attributes in the FlightOption schema.
                - **Total Cost Savings**: The total amount of potential savings identified.
                - **Cost Breakdown**: A detailed breakdown of costs per flight option.
                - **Alternative Routes**: Suggested alternative routes or flights that could offer additional benefits.
                - **Analysis Details**: Information on the criteria and methods used in the analysis.
                - **Recommendations**: Actionable recommendations for the user.
                - **Potential Challenges**: Any challenges or considerations the user should be aware of.
                - **Additional Notes**, **Resources**, **Contact Information**, **Legal Disclaimer**: Provide any additional relevant information.

                Provide your output in **JSON format** matching the **FlightAnalysis** schema below.

                **FlightAnalysis Schema**:

                {flight_analysis_schema}
            """),
            agent=agent,
            expected_output=f"The flight analysis report in JSON format matching the FlightAnalysis schema: {flight_analysis_schema}",
        )