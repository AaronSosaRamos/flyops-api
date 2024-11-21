from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
from crewai.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@tool
def wikipedia_search(query: str) -> str:
    """Search for information on Wikipedia."""
    api_wrapper = WikipediaAPIWrapper()
    return WikipediaQueryRun(api_wrapper=api_wrapper).run(query)

@tool
def tavily_search(query: str) -> str:
    """Perform a search with Tavily, including answers and raw content."""

    tavily_search_wrapper = TavilySearchAPIWrapper()

    return tavily_search_wrapper.results(query=query, max_results=5, search_depth="advanced")

class FlyOpsResearcherAgents:
    def __init__(self):
        self.OpenAIGPT4Mini = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-4o", temperature=0)
        self.tools = [
            wikipedia_search,
            tavily_search
        ]

    def flight_data_analyst_agent(self):
        return Agent(
            role="Flight Data Analyst",
            backstory=dedent("""You are an expert in analyzing large sets of flight data to identify trends, patterns, and anomalies."""),
            goal=dedent("""Analyze flight data within the specified date range and focus area to discover significant trends and insights that can impact the aviation industry."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def trend_analyst_agent(self):
        return Agent(
            role="Trend Analyst",
            backstory=dedent("""You specialize in interpreting data trends and predicting future developments in flight operations."""),
            goal=dedent("""Interpret analyzed data within the specified focus area to predict future trends in flight operations and suggest possible innovations."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def innovation_specialist_agent(self):
        return Agent(
            role="Innovation Specialist",
            backstory=dedent("""You identify and evaluate new innovations in flight data and technology that could revolutionize the industry."""),
            goal=dedent("""Identify key innovations in flight data and technology related to the focus area, and assess their potential impact on the industry."""),
            tools=self.tools,
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4Mini,
        )

    def research_report_generator_agent(self):
        return Agent(
            role="Research Report Generator",
            backstory=dedent("""You compile comprehensive research reports based on data analyses and insights, adhering to detailed schemas."""),
            goal=dedent("""Using the collected data and analyses, provide a comprehensive research report matching the FlightResearchReport schema, ensuring all fields are populated with detailed and accurate information."""),
            tools=[],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4,
        )
