import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

chat_history = [
    HumanMessage(content="Can LangSmith help test my LLM applications?"),
    AIMessage(content="Yes!"),
]

AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
prompt = ChatPromptTemplate.from_messages(
    messages=[
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        (
            "user",
            "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
        ),
    ]
)

prompt_template = ChatPromptTemplate.from_template(
    """
    Answer the following question based only on the provided context:
    <context>{context}</context>
    
    Question: {input}
    """
)

llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)


output_parser = StrOutputParser()

loader = WebBaseLoader(
    "https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/"
)
docs = loader.load()

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small", azure_deployment="shiun-text-embedding-3-small"
)


text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents=documents, embedding=embeddings)


document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)

# print(
#     document_chain.invoke(
#         {
#             "input": "Tell me what you see in the web, Your response is limited to 100 words",
#             "context": [
#                 Document(page_content="langsmith can let you visualize test results")
#             ],
#         }
#     )
# )

retriever = vector.as_retriever()
# retrieval_chain = create_retrieval_chain(
#     retriever=retriever, combine_docs_chain=document_chain
# )

# Tools
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="langsmith_search",
    description="Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

search = TavilySearchResults()
tools = [retriever_tool, search]

# Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(
    agent_executor.invoke(
        {"input": "how can langsmith help with testing?", "chat_history": chat_history}
    )
)
print(agent_executor.invoke({"input": "what is the weather in SF?"}))


retrieval_chain = create_history_aware_retriever(
    llm=llm, retriever=retriever, prompt=prompt
)

# print(
#     retrieval_chain.invoke(
#         {
#             "chat_history": chat_history,
#             "input": "Tell me now",
#         }
#     )
# )
