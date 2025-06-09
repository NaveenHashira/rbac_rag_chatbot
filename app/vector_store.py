import os
from typing import Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .document_loader import load_and_split_documents

class VectorStoreManager:
    def __init__(self, data_root: str = "data", embeddings_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector store manager.
        
        Args:
            data_root: Root directory containing department folders
            embeddings_model: Name of HuggingFace embeddings model
        """
        self.data_root = data_root
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.vector_stores: Dict[str, FAISS] = {}
        
    def _get_department_files(self, department: str) -> list:
        """Get all supported files for a department"""
        dept_path = os.path.join(self.data_root, department.lower())
        if not os.path.exists(dept_path):
            return []
            
        file_paths = []
        for root, _, files in os.walk(dept_path):
            for file in files:
                if file.endswith(('.pdf', '.md', '.txt', '.csv', '.markdown')):
                    file_paths.append(os.path.join(root, file))
        return file_paths

    def get_department_vectorstore(self, department: str) -> Optional[FAISS]:
        """
        Get or create vector store for a department.
        
        Args:
            department: Department name (case-insensitive)
            
        Returns:
            FAISS vectorstore if documents exist, None otherwise
        """
        department = department.lower()
        
        # Return cached vectorstore if available
        if department in self.vector_stores:
            return self.vector_stores[department]
            
        # Find and load department documents
        file_paths = self._get_department_files(department)
        if not file_paths:
            return None
            
        # Load and process documents
        docs = load_and_split_documents(file_paths)
        
        # Filter for department-specific docs (double-check)
        dept_docs = [
            doc for doc in docs 
            if doc.metadata.get('department', '').lower() == department
        ]
        
        if not dept_docs:
            return None
            
        # Create and cache vectorstore
        vectorstore = FAISS.from_documents(dept_docs, self.embeddings)
        self.vector_stores[department] = vectorstore
        return vectorstore

    def clear_cache(self):
        """Clear all cached vector stores"""
        self.vector_stores.clear()

    def get_available_departments(self) -> list:
        """
        Get list of departments with available documents.
        
        Returns:
            List of department names (capitalized)
        """
        if not os.path.exists(self.data_root):
            return []
            
        departments = []
        for item in os.listdir(self.data_root):
            if os.path.isdir(os.path.join(self.data_root, item)):
                if self._get_department_files(item):
                    departments.append(item.capitalize())
        return departments