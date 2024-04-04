import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Cloud Engineer"),
        ("human", "{input}"),
    ]
)

llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser
print(
    chain.invoke(
        {"input": "How do I monitor EC2 CPU, Your response is limited to 100 words"}
    )
)
