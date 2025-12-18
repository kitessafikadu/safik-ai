"""
Data Ingestion Script for ChromaDB RAG System
Loads content from JSON files, chunks text, generates embeddings, and stores in ChromaDB
"""

import os
import json
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configuration
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", str(Path(__file__).parent.parent / "chroma_db"))
COLLECTION_NAME_RAW = os.getenv("COLLECTION_NAME", "website_content")

def sanitize_collection_name(name: str) -> str:
    """
    Sanitize collection name to meet ChromaDB requirements:
    1. Contains 3-63 characters
    2. Starts and ends with an alphanumeric character
    3. Contains only alphanumeric characters, underscores, or hyphens
    4. Contains no two consecutive periods
    5. Is not a valid IPv4 address
    """
    if not name or not isinstance(name, str):
        name = "website_content"
    
    # Remove invalid characters (keep only alphanumeric, underscore, hyphen)
    import re
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    
    # Remove consecutive periods
    name = re.sub(r'\.\.+', '_', name)
    
    # Ensure it starts and ends with alphanumeric
    name = name.strip('_-')
    
    # Handle empty string after stripping
    if not name:
        name = "website_content"
    
    # Ensure starts with alphanumeric
    if name and not name[0].isalnum():
        name = 'a' + name
    
    # Ensure ends with alphanumeric
    if name and not name[-1].isalnum():
        name = name + '1'
    
    # Ensure length is between 3-63
    if len(name) < 3:
        name = name.ljust(3, '0')
    elif len(name) > 63:
        name = name[:63]
        if not name[-1].isalnum():
            name = name[:-1] + '0'
    
    return name

COLLECTION_NAME = sanitize_collection_name(COLLECTION_NAME_RAW)

# Paths
CONTENT_DIR = Path(__file__).parent.parent / "data" / "content"

def load_json_content(file_path: Path) -> dict:
    """Load content from a JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_documents_from_json(data: dict, source_file: str) -> list[Document]:
    """Extract documents from JSON structure"""
    documents = []
    page_name = data.get("page", "Unknown")

    # Handle different JSON structures
    if "sections" in data:
        # Homepage, About, Pricing structure
        for section in data["sections"]:
            if "title" in section and "content" in section:
                text = f"{section['title']}\n\n{section['content']}"
                metadata = {
                    "source": source_file,
                    "page": page_name,
                    "section": section["title"]
                }
            elif "tier" in section:  # Pricing tiers
                text = f"{section['tier']}\n\nPrice: {section.get('price', 'N/A')}\n\n{section['description']}\n\nIncludes: {section.get('includes', '')}"
                metadata = {
                    "source": source_file,
                    "page": page_name,
                    "section": section["tier"]
                }
            else:
                continue

            documents.append(Document(page_content=text, metadata=metadata))

    elif "questions" in data:
        # FAQ structure
        for qa in data["questions"]:
            text = f"Question: {qa['question']}\n\nAnswer: {qa['answer']}"
            metadata = {
                "source": source_file,
                "page": page_name,
                "question": qa["question"]
            }
            documents.append(Document(page_content=text, metadata=metadata))

    elif "studies" in data:
        # Case studies structure
        for study in data["studies"]:
            text = f"Client: {study['client']}\n\nChallenge: {study['challenge']}\n\nSolution: {study['solution']}\n\nResults: {study['results']}"
            metadata = {
                "source": source_file,
                "page": page_name,
                "client": study["client"]
            }
            documents.append(Document(page_content=text, metadata=metadata))

    return documents

def load_all_content() -> list[Document]:
    """Load all JSON content files from data/content directory"""
    all_documents = []

    json_files = list(CONTENT_DIR.glob("*.json"))
    print(f"Found {len(json_files)} JSON files to process")

    for json_file in json_files:
        print(f"Loading: {json_file.name}")
        data = load_json_content(json_file)
        source_name = json_file.stem  # filename without extension
        documents = extract_documents_from_json(data, source_name)
        all_documents.extend(documents)
        print(f"  Extracted {len(documents)} documents from {json_file.name}")

    return all_documents

def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller chunks for better retrieval"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # ~250 tokens
        chunk_overlap=200,  # Overlap to maintain context
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunked_docs = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunked_docs)} chunks")

    return chunked_docs

def ingest_to_chromadb(documents: list[Document]):
    """Ingest documents into ChromaDB with embeddings"""
    print(f"\nConnecting to ChromaDB at {PERSIST_DIRECTORY}...")

    # Create persist directory if it doesn't exist
    persist_path = Path(PERSIST_DIRECTORY)
    persist_path.mkdir(parents=True, exist_ok=True)

    # Clear existing data by deleting the directory (optional - comment out if you want to keep existing data)
    print(f"Clearing existing data from {PERSIST_DIRECTORY}...")
    if persist_path.exists():
        shutil.rmtree(persist_path)
        persist_path.mkdir(parents=True, exist_ok=True)

    # Initialize embeddings model
    print("Initializing HuggingFace embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create vector store and add documents
    print(f"Generating embeddings and storing {len(documents)} documents...")
    print("This may take a few minutes depending on the amount of content...\n")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )

    print(f"✅ Successfully ingested {len(documents)} documents into ChromaDB!")
    print(f"   Persist Directory: {PERSIST_DIRECTORY}")
    print(f"   Collection: {COLLECTION_NAME}")

    # Verify data
    doc_count = vector_store._collection.count()
    print(f"\n📊 Total documents in collection: {doc_count}")

    # Show sample document
    if doc_count > 0:
        results = vector_store.similarity_search("", k=1)
        if results:
            sample = results[0]
            print(f"\n📄 Sample document structure:")
            print(f"   - text: {sample.page_content[:100]}...")
            print(f"   - metadata: {sample.metadata}")

def main():
    """Main ingestion pipeline"""
    print("=" * 60)
    print("ChromaDB RAG - Data Ingestion Script")
    print("=" * 60)

    # Step 1: Load all content
    print("\n📁 Step 1: Loading content from JSON files...")
    documents = load_all_content()
    print(f"✅ Loaded {len(documents)} documents")

    # Step 2: Chunk documents
    print("\n✂️  Step 2: Chunking documents...")
    chunked_docs = chunk_documents(documents)
    print(f"✅ Created {len(chunked_docs)} chunks")

    # Step 3: Ingest to ChromaDB
    print("\n🚀 Step 3: Ingesting to ChromaDB with embeddings...")
    ingest_to_chromadb(chunked_docs)

    print("\n" + "=" * 60)
    print("✅ Data ingestion complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify data in ChromaDB (stored in chroma_db directory)")
    print("2. Build the RAG backend (rag_system.py & main.py)")
    print("3. Test the chatbot!")

if __name__ == "__main__":
    main()
