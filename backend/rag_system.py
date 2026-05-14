"""
RAG System using LangChain, ChromaDB Vector Store, and HuggingFace
"""

import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import requests

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


def load_documents_from_content_dir(content_dir: Path):
    documents = []

    for json_file in content_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)

        page_name = data.get("page", json_file.stem)

        if "sections" in data:
            for section in data["sections"]:
                if "title" in section and "content" in section:
                    text = f"{section['title']}\n\n{section['content']}"
                    metadata = {
                        "source": json_file.stem,
                        "page": page_name,
                        "section": section["title"],
                    }
                elif "tier" in section:
                    text = f"{section['tier']}\n\nPrice: {section.get('price', 'N/A')}\n\n{section['description']}\n\nIncludes: {section.get('includes', '')}"
                    metadata = {
                        "source": json_file.stem,
                        "page": page_name,
                        "section": section["tier"],
                    }
                else:
                    continue

                documents.append({"page_content": text, "metadata": metadata})

        elif "questions" in data:
            for qa in data["questions"]:
                text = f"Question: {qa['question']}\n\nAnswer: {qa['answer']}"
                metadata = {
                    "source": json_file.stem,
                    "page": page_name,
                    "question": qa["question"],
                }
                documents.append({"page_content": text, "metadata": metadata})

        elif "studies" in data:
            for study in data["studies"]:
                text = f"Client: {study['client']}\n\nChallenge: {study['challenge']}\n\nSolution: {study['solution']}\n\nResults: {study['results']}"
                metadata = {
                    "source": json_file.stem,
                    "page": page_name,
                    "client": study["client"],
                }
                documents.append({"page_content": text, "metadata": metadata})

    return documents


class RAGSystem:
    """RAG system for answering questions about Safik AI - OPTIMIZED for low memory"""

    def __init__(self):
        """Initialize the RAG system with ChromaDB and optional HuggingFace Inference API"""
        print("Initializing RAG system (optimized for low memory)...")

        self.vector_store = None
        self.retriever = None
        self.fallback_documents = []
        self.use_vector_store = False
        self.hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)
        self.hf_api_enabled = bool(self.hf_api_token)

        # Try to load ChromaDB (no embedding model needed for default backend)
        try:
            print(f"Loading ChromaDB vector store from {PERSIST_DIRECTORY}...")
            self.vector_store = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                collection_name=COLLECTION_NAME
            )

            # Try to retrieve to verify it works
            test_result = self.vector_store.similarity_search("AI services", k=1)
            if test_result:
                print("✓ ChromaDB loaded successfully with existing data")
                self.retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 4}
                )
                self.use_vector_store = True
            else:
                print("⚠ ChromaDB empty or not properly initialized")
                self.use_vector_store = False
        except Exception as e:
            print(f"⚠ ChromaDB not available: {e}")
            self.use_vector_store = False

        # Load fallback documents for keyword search
        print("Loading fallback documents for keyword search...")
        content_dir = Path(__file__).parent.parent / "data" / "content"
        self.fallback_documents = load_documents_from_content_dir(content_dir)
        print(f"✓ Loaded {len(self.fallback_documents)} fallback documents")

        if self.hf_api_enabled:
            print("✓ HuggingFace Inference API enabled for better answer generation")
        else:
            print("ℹ HuggingFace Inference API not configured (set HUGGINGFACEHUB_API_TOKEN)")

        print("✅ RAG system initialized successfully!")

    def _generate_answer_with_api(self, question: str, context: str) -> str:
        """Generate answer using HuggingFace Inference API (lightweight)"""
        if not self.hf_api_enabled:
            return None

        try:
            prompt = f"""You are a helpful AI assistant for Safik AI, an AI services company.
Answer the user's question based on the provided context. Be professional, friendly, and informative.

Context from our knowledge base:
{context}

User Question: {question}

Answer:"""

            response = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-large",
                headers={"Authorization": f"Bearer {self.hf_api_token}"},
                json={"inputs": prompt, "parameters": {"max_length": 256}},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "").strip()
                    return self._clean_generated_text(text)
        except Exception as e:
            print(f"API generation failed: {e}")
        
        return None

    def _clean_generated_text(self, text: str) -> str:
        """Clean model or document-extracted text: remove leading 'Question:' or 'Answer:' labels."""
        if not text:
            return ""
        # Remove leading 'Question: ...' if the model echoed the question
        text = re.sub(r"^\s*Question\s*[:\-]\s*.*?(\n\n|\n)", "", text, flags=re.I|re.S)
        # Remove leading 'Answer:' or 'Answer -'
        text = re.sub(r"^\s*Answer\s*[:\-]\s*", "", text, flags=re.I)
        return text.strip()

    def _format_docs(self, docs):
        """Format retrieved documents into a single string"""
        if isinstance(docs, list) and len(docs) > 0:
            if hasattr(docs[0], 'page_content'):
                return "\n\n".join(doc.page_content for doc in docs)
            else:
                return "\n\n".join(doc["page_content"] for doc in docs)
        return ""

    def _tokenize(self, text: str):
        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def _fallback_retrieve(self, question: str, top_k: int = 4):
        """Keyword-based retrieval using token matching"""
        query_tokens = self._tokenize(question)
        scored_docs = []

        for doc in self.fallback_documents:
            doc_tokens = self._tokenize(doc["page_content"])
            # Score based on token overlap
            score = len(query_tokens & doc_tokens)
            if score > 0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored_docs[:top_k]]

    def _fallback_answer(self, question: str, relevant_docs):
        """Generate answer from relevant documents without LLM"""
        if not relevant_docs:
            return "I don't have information about that topic. Please ask about our AI services, pricing, case studies, or FAQ."

        # Combine context from top documents
        # Prefer API-generated answer when available
        context = self._format_docs(relevant_docs)
        if self.hf_api_enabled:
            api_answer = self._generate_answer_with_api(question, context)
            if api_answer:
                return api_answer

        # Extractive fallback: look for explicit 'Answer:' sections in docs
        for doc in relevant_docs:
            content = doc.page_content if hasattr(doc, 'page_content') else doc.get('page_content', '')
            # Try to find 'Answer:' lines
            m = re.search(r"Answer\s*[:\-]\s*(.+?)(?:\n\n|$)", content, flags=re.I|re.S)
            if m:
                return self._clean_generated_text(m.group(1).strip())

            # If doc formatted as 'Question: ...\n\nAnswer: ...', capture the answer after Question
            m2 = re.search(r"Question\s*[:\-].*?\n\nAnswer\s*[:\-]\s*(.+?)(?:\n\n|$)", content, flags=re.I|re.S)
            if m2:
                return self._clean_generated_text(m2.group(1).strip())

        # Otherwise return the first reasonably long paragraph that isn't a question
        paragraphs = [p.strip() for p in context.split('\n\n') if p.strip()]
        for p in paragraphs:
            if len(p) > 50 and not re.match(r"^\s*Question\s*[:\-]", p, flags=re.I):
                return self._clean_generated_text(p[:1000])

        return "I found related content but need more context to answer fully."
    
    
    def ask(self, question: str) -> dict:
        """
        Ask a question and get an answer with sources

        Args:
            question: The user's question

        Returns:
            dict with 'answer' and 'sources' keys
        """
        # Try vector store first, then fallback to keyword search
        relevant_docs = []
        
        if self.use_vector_store and self.retriever:
            try:
                relevant_docs = self.retriever.invoke(question)
            except Exception as e:
                print(f"Vector store query failed: {e}, falling back to keyword search")
                relevant_docs = self._fallback_retrieve(question)
        else:
            relevant_docs = self._fallback_retrieve(question)
        
        # Generate answer
        answer = self._fallback_answer(question, relevant_docs)
        
        # Extract source information
        sources = []
        seen_sources = set()
        
        for doc in relevant_docs:
            metadata = doc.metadata if hasattr(doc, "metadata") else doc["metadata"]
            source_info = metadata.get("page", "Unknown")

            # Add section or question info if available
            if "section" in metadata:
                source_info = f"{source_info} - {metadata['section']}"
            elif "question" in metadata:
                source_info = f"FAQ: {metadata['question']}"

            # Avoid duplicate sources
            if source_info not in seen_sources:
                sources.append(source_info)
                seen_sources.add(source_info)

        return {
            "answer": answer,
            "sources": sources[:3],  # Return top 3 sources
            "num_sources": len(relevant_docs)
        }

    def close(self):
        """Close ChromaDB connection"""
        # ChromaDB handles persistence automatically, no explicit close needed
        pass


# Singleton instance
_rag_system = None


def get_rag_system() -> RAGSystem:
    """Get or create the RAG system singleton"""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
    return _rag_system


if __name__ == "__main__":
    # Test the RAG system
    print("\n" + "=" * 60)
    print("Testing RAG System")
    print("=" * 60)

    rag = get_rag_system()

    # Test questions
    test_questions = [
        "What AI services do you offer?",
        "Tell me about your pricing",
        "How long does implementation take?",
        "What's your favorite pizza?"  # Should say "I don't know"
    ]

    for question in test_questions:
        print(f"\n❓ Question: {question}")
        result = rag.ask(question)
        print(f"💬 Answer: {result['answer']}")
        print(f"📚 Sources: {', '.join(result['sources'])}")
        print("-" * 60)

    rag.close()
