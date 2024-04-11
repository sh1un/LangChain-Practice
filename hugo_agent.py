import os

from dotenv import find_dotenv, load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain.tools import StructuredTool
from langchain_openai import AzureChatOpenAI

from hugo_tools import (
    ask_for_more_information,
    check_knowledge_base,
    get_customer_messages,
    give_solution,
    open_ticket,
    rethink_solution,
)


def build_agent(prompt: str):

    _ = load_dotenv(find_dotenv())

    azure_deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME")

    llm = AzureChatOpenAI(
        azure_deployment=azure_deployment_name,  # change different model here!
        model_version="0613",
        api_version="2023-05-15",
    )

    tools = [
        StructuredTool.from_function(get_customer_messages),
        StructuredTool.from_function(check_knowledge_base),
        StructuredTool.from_function(ask_for_more_information),
        StructuredTool.from_function(give_solution),
        StructuredTool.from_function(rethink_solution),
        StructuredTool.from_function(open_ticket),
    ]

    agent_executor = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        return_intermediate_steps=True,
    )

    return agent_executor(prompt)
