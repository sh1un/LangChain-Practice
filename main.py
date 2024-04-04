import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")

llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)

print(llm.invoke(input="Hello I am shiun"))
