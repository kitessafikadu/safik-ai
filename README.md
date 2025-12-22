# Safik AI

Safik AI is Web App with a retrieval augmented generation (RAG) system that powers an AI chatbot using ChromaDB vector store, LangChain, and HuggingFace embeddings. This system allows users to ask questions about company services, pricing, and information stored in a knowledge base.

## 🚀 Features

- **RAG-Powered Chatbot**: Ask questions and get accurate answers based on company knowledge base
- **Vector Search**: Uses ChromaDB for efficient similarity search and retrieval
- **Real-time Responses**: Fast API responses powered by FastAPI backend
- **Responsive UI**: Modern, mobile-friendly interface with hamburger menu navigation
- **Source Citations**: Answers include source references from the knowledge base
- **Suggested Questions**: Quick access to common questions

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for developing applications powered by language models
- **ChromaDB** - Vector database for storing and querying embeddings
- **HuggingFace Transformers** - Pre-trained models for embeddings and LLM
- **Sentence Transformers** - For generating semantic embeddings
- **Python 3.12+**

### Frontend

- **Next.js 14** - React Framework for the Web
- **React** - Library for web and native user interfaces
- **TypeScript** - Strongly typed programming language
- **CSS3** - Ported legacy styles for consistent design
- **Inter Font** - Clean, modern typography

## 📁 Project Structure

```
RAG-System/
├── backend/
│   ├── main.py              # FastAPI server and endpoints
│   ├── rag_system.py        # RAG system implementation
│   ├── ingest_data.py       # Data ingestion script
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── app/                # Next.js App Router pages
│   ├── components/         # React components
│   ├── public/             # Static assets
│   ├── next.config.mjs     # Next.js configuration
│   └── package.json        # Frontend dependencies
├── data/
│   └── content/            # Knowledge base JSON files
│       ├── about.json
│       ├── services.json
│       ├── pricing.json
│       ├── faq.json
│       ├── case_studies.json
│       └── homepage.json
├── chroma_db/              # ChromaDB vector store (generated)
└── README.md
```

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kitessafikadu/safik-ai.git
cd safik-ai
```

### Step 2: Set Up Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will install PyTorch and transformers which may take some minutes 

## 🚀 Usage

### Starting the Backend Server

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

You can also use uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Viewing the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies (first time only):
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open `http://localhost:3000` in your browser.

### Using the Chatbot

1. Navigate to the chatbot page
2. Type your question in the input field
3. Click send or press Enter
4. View the answer with source citations

## 🔌 API Endpoints

### Health Check

```
GET /
```

Returns server status.

### Chat Endpoint

```
POST /api/chat
Content-Type: application/json

{
  "question": "What AI services do you offer?"
}
```

**Response:**

```json
{
  "answer": "We offer six main AI services...",
  "sources": ["Services - RAG Systems", "Services - Conversational AI"]
}
```

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file in the `backend/` directory:

```env
PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=website_content
```

### Default Configuration

- **Persistence Directory**: `./chroma_db` (relative to backend)
- **Collection Name**: `website_content`
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM Model**: `google/flan-t5-base`
- **Retrieval**: Top 4 most relevant chunks (k=4)

## 📝 Knowledge Base Format

The knowledge base files in `data/content/` should be JSON files with the following structures:

### Services/About/Pricing Format

```json
{
  "page": "Services",
  "sections": [
    {
      "title": "Section Title",
      "content": "Section content..."
    }
  ]
}
```

### FAQ Format

```json
{
  "page": "FAQ",
  "questions": [
    {
      "question": "Question text?",
      "answer": "Answer text..."
    }
  ]
}
```

### Case Studies Format

```json
{
  "page": "Case Studies",
  "studies": [
    {
      "client": "Client Name",
      "challenge": "Challenge description",
      "solution": "Solution description",
      "results": "Results description"
    }
  ]
}
```

## 🧪 Testing

Test the RAG system directly:

```bash
cd backend
python rag_system.py
```

This will run a series of test questions and display results.

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Hamburger Menu**: Mobile-friendly navigation menu
- **Smooth Animations**: Polished UI with smooth transitions
- **Typing Indicator**: Visual feedback while waiting for responses
- **Source Tags**: Clickable source references in responses
- **Suggested Questions**: Quick access buttons for common queries

## 🔧 Development

### Adding New Content

1. Add or modify JSON files in `data/content/`
2. Run the ingestion script again:
   ```bash
   python ingest_data.py
   ```
   **Note**: This will clear existing data and rebuild the vector store.

### Modifying the RAG System

Edit `backend/rag_system.py` to:

- Change the embedding model
- Modify retrieval parameters (k value, search type)
- Update the prompt template
- Change the LLM model

### Customizing the Frontend

- Edit `frontend/app/globals.css` for styling
- Modify React components in `frontend/components/`
- Update pages in `frontend/app/`

## 📚 Dependencies

Key Python packages:

- `fastapi==0.115.0` - Web framework
- `uvicorn[standard]==0.32.0` - ASGI server
- `langchain==0.3.7` - LLM framework
- `langchain-huggingface` - HuggingFace integration
- `chromadb==0.4.22` - Vector database
- `transformers==4.40.0` - HuggingFace transformers
- `sentence-transformers==2.7.0` - Sentence embeddings
- `torch==2.4.0` - PyTorch (for transformers)

## 🐛 Troubleshooting

### Import Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### ChromaDB Collection Errors

- Collection name is automatically sanitized to meet ChromaDB requirements
- If issues persist, delete `chroma_db/` folder and re-ingest data

### Model Download Issues

- First run will download models (~500MB for embeddings, ~1GB for LLM)
- Ensure stable internet connection
- Models are cached after first download

### Port Already in Use

- Change port in `main.py` or use: `uvicorn main:app --port 8001`

---

**Built with ❤️ using FastAPI, LangChain, and ChromaDB**
