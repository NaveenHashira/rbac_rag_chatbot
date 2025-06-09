from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os

def setup_rag_chain(vectorstore, groq_api_key: str):
    """
    Set up RAG chain with Groq
    
    Args:
        vectorstore: FAISS vector store
        groq_api_key: GROQ API key
        
    Returns:
        RetrievalQA: Configured RAG chain
    """

    llm = ChatGroq(
        temperature=1,
        groq_api_key=groq_api_key,
        model_name="Llama3-8b-8192"
    )
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

def handle_query(rag_chain, query: str):
    """
    Handle user query with RAG chain
    
    Args:
        rag_chain: Configured RAG chain
        query: User question
        
    Returns:
        str: Generated response
    """
    result = rag_chain.invoke({"query": query})
    return result["result"]