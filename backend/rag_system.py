"""
RAG System using LangChain, ChromaDB Vector Store, and HuggingFace
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from transformers import pipeline

# Load environment variables
load_dotenv()

# Configuration
PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", str(Path(__file__).parent.parent / "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "website_content")


class RAGSystem:
    """RAG system for answering questions about Safik AI"""

    def __init__(self):
        """Initialize the RAG system with ChromaDB vector store and HuggingFace"""
        print("Initializing RAG system...")

        # Initialize embeddings model
        print("Loading HuggingFace embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB vector store
        print(f"Loading ChromaDB vector store from {PERSIST_DIRECTORY}...")
        self.vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings,
            collection_name=COLLECTION_NAME
        )

        # Initialize LLM using HuggingFace
        print("Loading HuggingFace LLM...")
        # Using a lightweight instruction-following model
        model_name = "google/flan-t5-base"
        try:
            hf_pipeline = pipeline(
                "text2text-generation",
                model=model_name,
                max_length=512,
                temperature=0.7,
            )
            self.llm = HuggingFacePipeline(pipeline=hf_pipeline)
        except Exception as e:
            print(f"Warning: Could not load HuggingFace LLM: {e}")
            print("Falling back to a simple text-based approach.")
            # Fallback: use a simple text completion approach
            from langchain.llms.base import LLM
            from typing import Optional, List
            
            class SimpleLLM(LLM):
                def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
                    # Extract the question from the prompt
                    if "User Question:" in prompt:
                        question = prompt.split("User Question:")[-1].strip()
                        return f"Based on the context provided, I understand you're asking: {question}. Please configure a proper HuggingFace LLM model for full functionality."
                    return "Please configure a proper LLM model for full functionality."
                
                @property
                def _llm_type(self) -> str:
                    return "simple"
            
            self.llm = SimpleLLM()

        # Create retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
        )

        # Create prompt template
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

        # Create RAG chain
        self.rag_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        print("✅ RAG system initialized successfully!")

    def _format_docs(self, docs):
        """Format retrieved documents into a single string"""
        return "\n\n".join(doc.page_content for doc in docs)
    
    
    def ask(self, question: str) -> dict:
        """
        Ask a question and get an answer with sources

        Args:
            question: The user's question

        Returns:
            dict with 'answer' and 'sources' keys
        """
        # Get relevant documents
        relevant_docs = self.retriever.invoke(question)

        # Generate answer
        answer = self.rag_chain.invoke(question)
        
        # Extract source information
        sources = []
        seen_sources = set()
        
        for doc in relevant_docs:
            metadata = doc.metadata
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
