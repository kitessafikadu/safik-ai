"""
Check memory usage of initialized RAG system
"""

import os
import sys
import psutil
import tracemalloc
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Start memory tracking
tracemalloc.start()
initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

print(f"Initial Memory: {initial_memory:.2f} MB\n")

sys.path.insert(0, str(Path(__file__).parent))

print("Initializing RAG system...")
from rag_system import get_rag_system

rag = get_rag_system()
current_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
memory_used = current_memory - initial_memory

print(f"\n{'='*50}")
print(f"Memory Usage Report")
print(f"{'='*50}")
print(f"Initial Memory:      {initial_memory:.2f} MB")
print(f"Current Memory:      {current_memory:.2f} MB")
print(f"Used by RAG System:  {memory_used:.2f} MB")
print(f"\n✅ Total: {current_memory:.2f} MB (Render limit: 512 MB)")
print(f"📊 Usage: {(current_memory/512)*100:.1f}% of available memory\n")

if current_memory < 300:
    print("🎉 EXCELLENT - System uses minimal memory!")
elif current_memory < 512:
    print("✅ GOOD - Fits comfortably in Render free tier")
else:
    print("⚠️  WARNING - Approaching memory limit")

current, peak = tracemalloc.get_traced_memory()
print(f"\nPython allocated: {current / 1024 / 1024:.2f} MB (peak: {peak / 1024 / 1024:.2f} MB)")

tracemalloc.stop()
