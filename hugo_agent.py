import os

from dotenv import find_dotenv, load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent, AgentType
from hugo_tools import realize_the_problem, categorize_the_problem, find_solutions, report_the_problem

def build_agent(prompt: str):

    _ = load_dotenv(find_dotenv())

    azure_deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME")

    llm = AzureChatOpenAI(
        azure_deployment=azure_deployment_name,
        model_version="0613",
        api_version="2023-05-15",
    )

    tools = [
        StructuredTool.from_function(realize_the_problem),
        StructuredTool.from_function(categorize_the_problem),
        StructuredTool.from_function(find_solutions),
        StructuredTool.from_function(report_the_problem),
    ]

    agent_executor = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        return_intermediate_steps=True,
    )


    return agent_executor(prompt)