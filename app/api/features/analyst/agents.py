from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@tool
def wikipedia_search(query: str) -> str:
    """Search for information on Wikipedia."""
    api_wrapper = WikipediaAPIWrapper()
    return WikipediaQueryRun(api_wrapper=api_wrapper).run(query)

@tool
def serp_api_search(query: str) -> str:
    """Look up information using SerpAPI."""
    serp_api = SerpAPIWrapper()
    return serp_api.run(query)

@tool
def tavily_search(query: str) -> str:
    """Perform a search with Tavily, including answers and raw content."""
    tavily = TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=True
    )
    return tavily.run(query)

class FlyOpsAnalystAgents:
    def __init__(self):
        self.OpenAIGPT4Mini = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4o", temperature=0)
        self.tools = [
            wikipedia_search,
            serp_api_search,
            tavily_search
        ]

    def flight_data_collector_agent(self):
        return Agent(
            role="Flight Data Collector",
            backstory=dedent("""You are an expert in gathering real-time flight information based on user input. You utilize tools to collect accurate and up-to-date flight data."""),
            goal=dedent("""Collect available flights from the specified origin to the destination on the given date within the user's available budget, including detailed flight information as per the FlightOption schema."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def flight_optimizer_agent(self):
        return Agent(
            role="Flight Optimizer",
            backstory=dedent("""You specialize in analyzing flight options to recommend the best flights considering factors like price, duration, stops, and amenities."""),
            goal=dedent("""Analyze the collected flight data and recommend the best flight options to the user, including detailed justifications and potential cost savings."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def cost_analysis_agent(self):
        return Agent(
            role="Cost Analysis Agent",
            backstory=dedent("""You provide insights on how the user can save costs on their flights and offer detailed cost breakdowns and alternative options."""),
            goal=dedent("""Identify potential cost savings, provide a cost breakdown, and suggest alternative routes or options that could reduce expenses while meeting the user's needs."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def report_generator_agent(self):
        return Agent(
            role="Report Generator",
            backstory=dedent("""You compile all the information from the previous analyses and provide a comprehensive flight analysis report to the user, adhering to the detailed FlightAnalysis schema."""),
            goal=dedent("""Using the collected flight data and analyses, provide a comprehensive flight analysis report matching the FlightAnalysis schema, ensuring all fields are populated with detailed and accurate information."""),
            tools=[],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )
