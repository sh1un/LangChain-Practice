import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from langchain_openai import AzureChatOpenAI
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Variables
load_dotenv(override=True)
FILE_PATH = Path("C:/GitHub/LangChain-Practice/mediumblog.txt")

# Pinecone
index_name = "mediumblog-index"

# LLM
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)

if __name__ == "__main__":
    print("Hello, World!")
    loader = TextLoader(str(FILE_PATH), encoding="utf-8")
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    texts = text_splitter.split_documents(document)
    print(len(texts))

    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-small", azure_deployment="shiun-text-embedding-3-small"
    )
    pinecone_index = Pinecone.from_existing_index(index_name, embeddings)
    docsearch = PineconeVectorStore.from_documents(
        texts, embedding=embeddings, index_name=index_name
    )

    # RetrievalQA
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    query = "What is a vector db? Give me a 15 word answer for a beginner."
    result = qa.invoke({"query": query})
    print(result)
