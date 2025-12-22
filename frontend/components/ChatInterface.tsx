"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  sources?: string[];
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init",
      text: "Hello! I'm the Safik AI assistant. I can help you learn about our AI services, pricing, case studies, and answer questions about our company. What would you like to know?",
      sender: "bot",
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    // Auto-resize
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        Math.min(textareaRef.current.scrollHeight, 120) + "px";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }

    // Add user message
    const newUserMsg: Message = {
      id: Date.now().toString(),
      text: userMessage,
      sender: "user",
    };
    setMessages((prev) => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      const newBotMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        sender: "bot",
        sources: data.sources,
      };
      setMessages((prev) => [...prev, newBotMsg]);
    } catch (error) {
      console.error("Error:", error);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: "I apologize, but I'm currently unable to process your request. This could be because the backend server is not running yet. Please make sure the FastAPI server is started and try again.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: "init",
        text: "Hello! I'm the Safik AI assistant. I can help you learn about our AI services, pricing, case studies, and answer questions about our company. What would you like to know?",
        sender: "bot",
      },
    ]);
  };

  const handleSuggestedClick = (text: string) => {
    setInputValue(text);
    // Determine if we should send immediately or let user edit?
    // app.js sent immediately
    // Ideally we update state then send, but state update is async.
    // Let's just set it and trigger send logic manually or just call send with the text.
    // But inputValue is bound to textarea.
    // Let's just set the input value for now and focus, or replicate app.js behavior which was click -> send.
    // To do click -> send we need to bypass the input state or handle it carefully.
    // Easier: just set input, let user send? Or simulate send.
    // App.js behavior: "chatInput.value = pill.textContent; sendButton.disabled = false; sendMessage();"
    // So it sends immediately.
    // Refactored sendMessage to accept text?
    sendText(text);
  };

  const sendText = async (text: string) => {
    if (isLoading) return;
    const userMessage = text;
    
    // Add user message
    const newUserMsg: Message = {
      id: Date.now().toString(),
      text: userMessage,
      sender: "user",
    };
    setMessages((prev) => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      const newBotMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        sender: "bot",
        sources: data.sources,
      };
      setMessages((prev) => [...prev, newBotMsg]);
    } catch (error) {
      console.error("Error:", error);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        text: "I apologize, but I'm currently unable to process your request. This could be because the backend server is not running yet. Please make sure the FastAPI server is started and try again.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <section className="chatbot-section">
      <div className="container">
        <div className="chatbot-header-text">
          <h1>AI-Powered Assistant</h1>
          <p>
            Ask me anything about Safik AI&apos;s services, pricing, or
            capabilities
          </p>
        </div>

        <div className="chatbot-container">
          <div className="chat-header">
            <div className="chat-status">
              <div className="status-indicator"></div>
              <span>AI Assistant Online</span>
            </div>
            <button className="clear-chat" onClick={clearChat} title="Clear Chat">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M4 4L16 16M16 4L4 16"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </button>
          </div>

          <div className="chat-messages" id="chatMessages">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`message ${msg.sender === "bot" ? "bot-message" : "user-message"}`}
              >
                <div className="message-avatar">
                  {msg.sender === "bot" ? (
                    <Image 
                      src="/bot.png" 
                      alt="AI Assistant" 
                      width={24} 
                      height={24} 
                      className="bot-avatar-img"
                      style={{ borderRadius: '6px' }}
                    />
                  ) : (
                    "U"
                  )}
                </div>
                <div className="message-content">
                  <div className="message-text">
                     {msg.text}
                     {msg.sources && msg.sources.length > 0 && (
                        <div className="message-sources">
                          <strong>Sources:</strong>
                          {msg.sources.map((source, index) => (
                            <span key={index} className="source-tag">{source}</span>
                          ))}
                        </div>
                     )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message bot-message">
                <div className="message-avatar">
                  <Image 
                    src="/bot.png" 
                    alt="AI Assistant" 
                    width={24} 
                    height={24} 
                    className="bot-avatar-img"
                    style={{ borderRadius: '6px' }}
                  />
                </div>
                <div className="message-content">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="suggested-questions">
            <div className="suggested-title">Suggested questions:</div>
            <div className="suggested-pills">
              <button
                className="suggested-pill"
                onClick={() => handleSuggestedClick("What AI services do you offer?")}
              >
                What AI services do you offer?
              </button>
              <button
                className="suggested-pill"
                onClick={() => handleSuggestedClick("Tell me about your pricing")}
              >
                Tell me about your pricing
              </button>
              <button
                className="suggested-pill"
                onClick={() => handleSuggestedClick("What industries do you work with?")}
              >
                What industries do you work with?
              </button>
              <button
                className="suggested-pill"
                onClick={() => handleSuggestedClick("How long does implementation take?")}
              >
                How long does implementation take?
              </button>
            </div>
          </div>

          <div className="chat-input-container">
            <div className="chat-input-wrapper">
              <textarea
                ref={textareaRef}
                className="chat-input"
                placeholder="Ask a question about our AI services..."
                rows={1}
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
              ></textarea>
              <button
                className="send-button"
                disabled={isLoading || inputValue.trim() === ""}
                onClick={sendMessage}
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path
                    d="M18 2L9 11M18 2L12 18L9 11M18 2L2 8L9 11"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div className="chatbot-info">
          <div className="info-card">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="#667eea"
                strokeWidth="2"
              />
              <path
                d="M12 8V12L14 14"
                stroke="#667eea"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <div>
              <h4>Real-time Responses</h4>
              <p>Powered by advanced RAG technology</p>
            </div>
          </div>
          <div className="info-card">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <rect
                x="3"
                y="3"
                width="18"
                height="18"
                rx="2"
                stroke="#667eea"
                strokeWidth="2"
              />
              <path
                d="M9 12L11 14L15 10"
                stroke="#667eea"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
            <div>
              <h4>Accurate Information</h4>
              <p>Answers backed by our knowledge base</p>
            </div>
          </div>
          <div className="info-card">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2L2 7L12 12L22 7L12 2Z"
                stroke="#667eea"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M2 17L12 22L22 17"
                stroke="#667eea"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M2 12L12 17L22 12"
                stroke="#667eea"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <div>
              <h4>Multi-source Search</h4>
              <p>ChromaDB Vector Search integration</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
