import os

from dotenv import load_dotenv
from langchain_community.chat_models.bedrock import BedrockChat
from langchain_core.messages import HumanMessage

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
AWS_CRED_PROFILE_NAME = os.environ.get("AWS_CRED_PROFILE_NAME")

chat = BedrockChat(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 1.0},
    credentials_profile_name=AWS_CRED_PROFILE_NAME,
)

messages = [HumanMessage(content="Hello I am shiun")]

print(chat(messages=messages))
