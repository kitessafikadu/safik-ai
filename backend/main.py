"""
FastAPI Server for ChromaDB RAG Chatbot
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_system import get_rag_system
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=" AI Chatbot API",
    description="RAG-powered chatbot using ChromaDB Vector Store",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    question: str

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What AI services do you offer?"
            }
        }


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "We offer six main AI services including RAG systems, conversational AI, custom ML models, AI strategy consulting, model fine-tuning, and vector database implementation.",
                "sources": ["Services - RAG Systems", "Services - Conversational AI", "Services - Custom ML Models"]
            }
        }


# Initialize RAG system on startup
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system when server starts"""
    logger.info("Starting up FastAPI server...")
    try:
        get_rag_system()
        logger.info("✅ RAG system initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG system: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down FastAPI server...")
    rag = get_rag_system()
    rag.close()
    logger.info("✅ Resources cleaned up")


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": " AI Chatbot API is running",
        "version": "1.0.0"
    }
    
    

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received question: {request.question}")

        # Validate question
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        if len(request.question) > 500:
            raise HTTPException(status_code=400, detail="Question too long (max 500 characters)")
        
        rag = get_rag_system()
        result = rag.ask(request.question)
        
        logger.info(f"Generated answer with {len(result['sources'])} sources")
 
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question. Please try again."
        )
    
    

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
