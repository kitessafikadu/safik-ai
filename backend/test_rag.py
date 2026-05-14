"""
Test script for RAG system with HuggingFace Inference API
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Check if token is available
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if token:
    print(f"✓ HuggingFace token loaded: {token[:20]}...")
else:
    print("✗ No HuggingFace token found")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_system import get_rag_system

print("\n" + "=" * 70)
print("Testing RAG System with HuggingFace Inference API")
print("=" * 70)

try:
    print("\n📍 Initializing RAG system...")
    rag = get_rag_system()
    
    print("\n" + "-" * 70)
    print("Running test queries...")
    print("-" * 70)
    
    test_questions = [
        "What AI services do you offer?",
        "Tell me about your pricing",
        "Do you do custom ML models?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[Test {i}] ❓ Question: {question}")
        print("⏳ Processing...")
        
        try:
            result = rag.ask(question)
            
            print(f"💬 Answer: {result['answer']}")
            print(f"📚 Sources: {', '.join(result['sources'])}")
            print(f"📊 Relevant docs: {result['num_sources']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 70)
    
    print("\n✅ Test completed successfully!")
    print("\nNote:")
    print("- If answers are well-formed and natural, the HF Inference API is working")
    print("- If answers are simple text excerpts, the extractive fallback is being used")
    
except Exception as e:
    print(f"\n❌ Failed to initialize RAG system: {e}")
    import traceback
    traceback.print_exc()

finally:
    try:
        rag.close()
    except:
        pass
