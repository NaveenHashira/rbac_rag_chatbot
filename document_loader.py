import os
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader, 
    CSVLoader, 
    UnstructuredPDFLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_department_from_path(file_path):
    """
    Extracts the department name from the file path based on the folder
    immediately under 'data/'.
    """
    parts = file_path.split(os.sep)
    if "data" in parts:
        idx = parts.index("data")
        if idx + 1 < len(parts):
            return parts[idx + 1].capitalize()
    return "Unknown"


def load_and_split_documents(file_paths, chunk_size=500, chunk_overlap=50):
    """
    Load and process documents from various file types: PDF, Markdown,
    TXT, and CSV.

    Parameters:
        file_paths (list[str]): List of file paths to load.
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between chunks.

    Returns:
        list: Processed list of Document objects with metadata.
    """
    text_docs = []
    other_docs = []

    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        docs = []

        if ext in ['.md', '.markdown']:
            loader = UnstructuredMarkdownLoader(file_path)
            docs = loader.load()

        elif ext == '.txt':
            loader = TextLoader(file_path)
            docs = loader.load()

        elif ext == '.pdf':
            loader = UnstructuredPDFLoader(file_path)
            docs = loader.load()

        elif ext == '.csv':
            loader = CSVLoader(file_path=file_path)
            docs = loader.load()
            department = get_department_from_path(file_path)
            for d in docs:
                d.metadata['department'] = department
            other_docs.extend(docs)
            continue

        else:
            print(f"Warning: Unsupported file type '{ext}' for '{file_path}'")
            continue

        # Assign department metadata to text documents
        department = get_department_from_path(file_path)
        for d in docs:
            d.metadata['department'] = department
        text_docs.extend(docs)

    # Split text-based documents only
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_text_docs = splitter.split_documents(text_docs)

    return split_text_docs + other_docs


if __name__ == "__main__":
    files = [
        "data/engineering/engineering_master_doc.md",
        "data/finance/financial_summary.md",
        "data/finance/quarterly_financial_report.md",
        "data/general/employee_handbook.md",
        "data/marketing/market_report_q4_2024.md",
        "data/marketing/marketing_report_2024.md",
        "data/marketing/marketing_report_q1_2024.md",
        "data/marketing/marketing_report_q2_2024.md",
        "data/marketing/marketing_report_q3_2024.md",
        "data/hr/hr_data.csv"

    ]
    

    all_docs = load_and_split_documents(files)
    print(f"Loaded {len(all_docs)} documents.")
