import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.readthedocs import ReadTheDocsLoader
from langchain_openai.chat_models.azure import AzureChatOpenAI
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

load_dotenv(override=True)

LANGCHAIN_DOCS_PATH = Path("C:/GitHub/LangChain-Practice/langchain-docs")


# Pinecone
index_name = "langchain-doc-index"

# LLM
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
)

# embedding model
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small", azure_deployment="shiun-text-embedding-3-small"
)


def ingest_docs() -> None:
    loader = ReadTheDocsLoader(path=LANGCHAIN_DOCS_PATH, encoding="utf-8")
    raw_documents = loader.load()
    print("Loaded documents: ", len(raw_documents))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documents)
    print("Split documents: ", len(documents), "chunks")

    # Update the source metadata to point to the correct URL
    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(
        embedding=embeddings, documents=documents, index_name=index_name
    )
    print("************** Added to Pinecone vector DB vectors **************")


if __name__ == "__main__":
    print("Hello, World!")
    ingest_docs()
