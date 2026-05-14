# Deployment Configuration for Render

## Frontend & Backend Integration

The RAG System is now configured for deployment on Render with the following setup:

### Environment Variables

#### Backend (Python/FastAPI)

- **Production URL**: `https://safik-ai.onrender.com`
- **Service Name**: `safik-ai-backend`
- **Environment Variable**: `HUGGINGFACEHUB_API_TOKEN` (optional, set in Render dashboard)

#### Frontend (Next.js)

- **Development**: Uses `http://localhost:8000` (from `.env.local`)
- **Production**: Uses `https://safik-ai.onrender.com` (from `.env.production`)

### Files

```
frontend/
├── .env.local          # Development (localhost) - NOT committed
├── .env.production     # Production (Render URL) - committed
└── components/
    └── ChatInterface.tsx  # Updated to use NEXT_PUBLIC_API_BASE_URL
```

### How It Works

1. **Development** (Local Testing)

   ```bash
   cd frontend
   npm run dev
   # Uses http://localhost:8000 from .env.local
   ```

2. **Production** (Render)
   - Frontend automatically uses `https://safik-ai.onrender.com` from `.env.production`
   - All API calls from ChatInterface use the production URL

### Deployment Steps

#### 1. Deploy Backend on Render

- Create a new Web Service
- Connect your GitHub repository
- Configure:
  - **Name**: `safik-ai-backend`
  - **Root Directory**: `backend`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
  - **Environment Variables**:
    - `HUGGINGFACEHUB_API_TOKEN=your_token_here` (optional, for better answers)

#### 2. Deploy Frontend on Render

- Create a new Static Site or Web Service
- Connect your GitHub repository
- Configure:
  - **Root Directory**: `frontend`
  - **Build Command**: `npm install && npm run build`
  - **Publish Directory**: `.next`
  - **Start Command**: `npm run start` (if using Web Service)
  - **Node Version**: `18` or higher

#### 3. API Configuration

After deployment, your frontend will automatically call:

```
https://safik-ai.onrender.com/api/chat
```

### Testing

#### Local Development

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000` and test the chat interface.

#### Production

Visit your frontend URL on Render and test the chat interface.

### Environment Variable Setup

**For Render Dashboard:**

Backend Service:

```
HUGGINGFACEHUB_API_TOKEN=hf_your_actual_token
```

Frontend Service:

- No environment variables needed (`.env.production` is in repo)

### Troubleshooting

#### CORS Issues

If you see CORS errors in browser console, the backend is already configured to allow all origins. Check:

- Backend is running and accessible
- API URL is correct in `.env.production`

#### API Not Responding

- Verify backend URL is correct: `https://safik-ai.onrender.com`
- Check Render dashboard for backend service status
- Check backend logs for errors

#### Token Issues

- Verify `HUGGINGFACEHUB_API_TOKEN` is set in Render dashboard (if using API)
- System works without token (uses extractive QA)

### Build Size Notes

**Frontend Build**: ~3-5MB (Next.js optimized)
**Backend**: Fits within 512MB limit ✅

### Performance

- **Frontend Response**: ~100-300ms (extractive QA)
- **With HF API**: ~1-3s per query (better quality)
- **Cold Start**: ~10s for backend (Render free tier)

### Next Steps

1. Commit and push to GitHub
2. Create Render services (backend first, then frontend)
3. Update `.env.production` if you change the backend URL
4. Monitor logs in Render dashboard
