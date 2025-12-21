# Safik AI - Frontend

This is the frontend application for Safik AI, built with [Next.js](https://nextjs.org). It provides a modern, responsive interface for exploring Safik AI's services and interacting with the RAG-powered chatbot.

## Features

- **Responsive Design**: Fully responsive layout adapted from the legacy HTML/CSS design.
- **RAG Chatbot**: Integrated chat interface connecting to the FastAPI backend.
- **Modern Stack**: Built with Next.js 14, React, and TypeScript.
- **Optimized Performance**: Uses Next.js features like server components and image optimization.

## Getting Started

### Prerequisites

- Node.js 18+ installed
- The backend FastAPI server running on `http://localhost:8000` (for chatbot functionality)

### Installation

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```

4.  Open [http://localhost:3000](http://localhost:3000) with your browser.

## Project Structure

- `app/`: Next.js app directory containing pages (`page.tsx`, `chatbot/page.tsx`) and layout.
- `components/`: Reusable React components (`Navbar`, `Footer`, `Hero`, `ChatInterface`, etc.).
- `app/globals.css`: Global styles (ported from legacy CSS).

## Backend Integration

The chatbot interface (`components/ChatInterface.tsx`) communicates with the backend API at `http://localhost:8000/api/chat`. Ensure the backend is running for the chat to function correctly.
