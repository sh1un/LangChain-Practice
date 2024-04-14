import os
from pathlib import Path

import pinecone
from dotenv import load_dotenv
from langchain.document_loaders.text import TextLoader
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone

# Variables
load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
FILE_PATH = Path("C:/GitHub/LangChain-Practice/mediumblog.txt")

# Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
pc.create_index("mediumblog-index", metric="cosine", shards=1, dimension=768)
index_name = "mediumblog-index"

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
    docsearch = pinecone_index.from_documents(texts, embedding=embeddings)
