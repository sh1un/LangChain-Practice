import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")

llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)

message = HumanMessage(content="Hello I am shiun")

print(llm([message]))
