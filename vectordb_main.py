from pathlib import Path

from dotenv import load_dotenv
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Variables
load_dotenv(override=True)
FILE_PATH = Path("C:/GitHub/LangChain-Practice/mediumblog.txt")

# Pinecone
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
    docsearch = PineconeVectorStore.from_documents(
        texts, embedding=embeddings, index_name=index_name
    )
