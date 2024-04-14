import os

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai.chat_models.azure import AzureChatOpenAI
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore

# Pinecone
index_name = "langchain-doc-index"

# LLM
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
llm = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_NAME,
    model_version="0613",
    api_version="2023-05-15",
    verbose=True,
)

# embedding model
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small", azure_deployment="shiun-text-embedding-3-small"
)


def run_llm(query: str) -> any:
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name, embedding=embeddings
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )

    return qa.invoke({"query": query})


if __name__ == "__main__":
    query = "What is LangChain?"
    result = run_llm(query)
    print(result)
