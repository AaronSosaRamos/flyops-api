from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SQL_PREFIX = """
You are an agent designed to interact with a SQL database.
Given an input question, generate a syntactically correct SQLite query to retrieve data, focusing only on `SELECT` statements.
You are restricted to read-only queries, so you may not use any data manipulation language (DML) or data definition language (DDL) commands like `INSERT`, `UPDATE`, `DELETE`, `DROP`, or `CREATE`.
Always begin by identifying the tables available in the database. You should query the schema of the relevant tables to understand their structure.
Construct your queries to retrieve only the necessary columns relevant to the user's question, limiting the results to a maximum of 5 unless otherwise specified.
Ensure your queries are well-formed, and if an error occurs, refine the query before attempting to execute it again.
You must follow these constraints at all times.
"""

system_message = SystemMessage(content=SQL_PREFIX)
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

def generate_response_assistant(query: str):
    db = SQLDatabase.from_uri("sqlite:///flyops_assistant.db")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()
    agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)
    result = agent_executor.invoke({"messages": [HumanMessage(content=query)]})

    return result['messages'][-1].content