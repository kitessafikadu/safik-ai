"""
RAG System using LangChain, ChromaDB Vector Store, and HuggingFace
"""

import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

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
    """RAG system for answering questions about Safik AI"""

    def __init__(self):
        """Initialize the RAG system with ChromaDB vector store and HuggingFace"""
        print("Initializing RAG system...")

        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.llm = None
        self.rag_chain = None
        self.fallback_documents = []
        self.use_fallback_mode = False

        try:
            print("Loading HuggingFace embeddings model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            print(f"Loading ChromaDB vector store from {PERSIST_DIRECTORY}...")
            self.vector_store = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=self.embeddings,
                collection_name=COLLECTION_NAME
            )

            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB retrieval: {e}")
            print("Falling back to keyword search over the source JSON content.")
            self.use_fallback_mode = True
            content_dir = Path(__file__).parent.parent / "data" / "content"
            self.fallback_documents = load_documents_from_content_dir(content_dir)

        self.prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant for Safik AI, an AI services company.
Answer the user's question based on the provided context. Be professional, friendly, and informative.

IMPORTANT INSTRUCTIONS:
- If the context contains relevant information, use it to answer the question
- Be specific and cite information from the context
- If the context doesn't contain enough information to fully answer the question, say so honestly
- Don't make up information that's not in the context
- Keep your answers concise but informative (2-4 sentences typically)
- Use a professional but approachable tone

Context from our knowledge base:
{context}

User Question: {question}

Answer:""")

        self._initialize_llm()

        if self.retriever is not None and self.llm is not None:
            self.rag_chain = (
                {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

        print("✅ RAG system initialized successfully!")

    def _initialize_llm(self):
        """Initialize the HuggingFace LLM, or keep a fallback if Torch is unavailable."""
        print("Loading HuggingFace LLM...")
        model_name = "google/flan-t5-base"

        try:
            from transformers import pipeline

            hf_pipeline = pipeline(
                "text2text-generation",
                model=model_name,
                max_length=512,
                temperature=0.7,
            )
            self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        except Exception as e:
            print(f"Warning: Could not load HuggingFace LLM: {e}")
            print("Falling back to extractive answers from the retrieved documents.")
            self.llm = None

    def _format_docs(self, docs):
        """Format retrieved documents into a single string"""
        return "\n\n".join(doc.page_content for doc in docs)

    def _tokenize(self, text: str):
        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def _fallback_retrieve(self, question: str):
        query_tokens = self._tokenize(question)
        scored_docs = []

        for doc in self.fallback_documents:
            doc_tokens = self._tokenize(doc["page_content"])
            score = len(query_tokens & doc_tokens)
            if score > 0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored_docs[:4]]

    def _fallback_answer(self, question: str, relevant_docs):
        if not relevant_docs:
            return (
                "I could not load the embedding model in this environment, so I am using a keyword-based fallback. "
                "I do not have enough matching content to answer that question confidently."
            )

        top_doc = relevant_docs[0]
        page_name = top_doc["metadata"].get("page", "Unknown")
        source_line = top_doc["page_content"].split("\n\n")[0]
        return f"I found related information in {page_name}. {source_line}"
    
    
    def ask(self, question: str) -> dict:
        """
        Ask a question and get an answer with sources

        Args:
            question: The user's question

        Returns:
            dict with 'answer' and 'sources' keys
        """
        if self.retriever is not None:
            relevant_docs = self.retriever.invoke(question)
            answer = self.rag_chain.invoke(question) if self.rag_chain is not None else self._fallback_answer(question, [])
        else:
            relevant_docs = self._fallback_retrieve(question)
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
