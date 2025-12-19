// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Hamburger menu toggle
  const hamburgerMenu = document.getElementById("hamburgerMenu");
  const navMenu = document.getElementById("navMenu");

  if (hamburgerMenu && navMenu) {
    hamburgerMenu.addEventListener("click", (e) => {
      e.stopPropagation(); // Prevent event from bubbling to document
      hamburgerMenu.classList.toggle("active");
      navMenu.classList.toggle("active");
    });

    // Close menu when clicking on a link
    navMenu.addEventListener("click", (e) => {
      if (e.target.tagName === "A") {
        hamburgerMenu.classList.remove("active");
        navMenu.classList.remove("active");
      }
    });

    // Close menu when clicking outside
    document.addEventListener("click", (e) => {
      // Only close if menu is active and click is outside both hamburger and menu
      if (
        navMenu.classList.contains("active") &&
        !hamburgerMenu.contains(e.target) &&
        !navMenu.contains(e.target)
      ) {
        hamburgerMenu.classList.remove("active");
        navMenu.classList.remove("active");
      }
    });
  }
});

// Chat application logic (only if elements exist - for chatbot page)
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendButton = document.getElementById("sendButton");
const clearChatButton = document.getElementById("clearChat");
const suggestedPills = document.querySelectorAll(".suggested-pill");

// API endpoint - will be updated when backend is ready
const API_ENDPOINT = "http://localhost:8000/api/chat";

// Auto-resize textarea
function autoResizeTextarea() {
  if (!chatInput) return;
  chatInput.style.height = "auto";
  chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + "px";
}

// Only initialize chat functionality if we're on the chatbot page
if (chatInput && sendButton && clearChatButton && chatMessages) {
  // Enable send button when input has content
  chatInput.addEventListener("input", () => {
    sendButton.disabled = chatInput.value.trim() === "";
    autoResizeTextarea();
  });

  // Send message on Enter (Shift+Enter for new line)
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Send button click
  sendButton.addEventListener("click", sendMessage);

  // Clear chat
  clearChatButton.addEventListener("click", () => {
    // Keep only the initial bot message
    const initialMessage = chatMessages.querySelector(".bot-message");
    chatMessages.innerHTML = "";
    chatMessages.appendChild(initialMessage.cloneNode(true));
  });

  // Suggested questions
  suggestedPills.forEach((pill) => {
    pill.addEventListener("click", () => {
      chatInput.value = pill.textContent;
      sendButton.disabled = false;
      sendMessage();
    });
  });
}

// Main send message function
async function sendMessage() {
  if (!chatInput || !sendButton || !chatMessages) return;
  const message = chatInput.value.trim();
  if (!message) return;

  // Add user message to chat
  addMessage(message, "user");

  // Clear input
  chatInput.value = "";
  sendButton.disabled = true;
  chatInput.style.height = "auto";

  // Show typing indicator
  const typingIndicator = addTypingIndicator();

  try {
    // Call API
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: message }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    // Remove typing indicator
    typingIndicator.remove();

    // Add bot response
    addMessage(data.answer, "bot", data.sources);
  } catch (error) {
    console.error("Error:", error);
    typingIndicator.remove();

    // Show error message
    addMessage(
      "I apologize, but I'm currently unable to process your request. This could be because the backend server is not running yet. Please make sure the FastAPI server is started and try again.",
      "bot"
    );
  }
}

// Add message to chat
function addMessage(text, sender, sources = null) {
  if (!chatMessages) return null;
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";

  if (sender === "bot") {
    avatar.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect width="24" height="24" rx="6" fill="url(#botGradient${Date.now()})"/>
                <path d="M6 12L9 9L12 12L15 9L18 12" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="botGradient${Date.now()}" x1="0" y1="0" x2="24" y2="24">
                        <stop offset="0%" stop-color="#667eea"/>
                        <stop offset="100%" stop-color="#764ba2"/>
                    </linearGradient>
                </defs>
            </svg>
        `;
  } else {
    avatar.textContent = "U";
  }

  const content = document.createElement("div");
  content.className = "message-content";

  const textDiv = document.createElement("div");
  textDiv.className = "message-text";
  textDiv.textContent = text;

  content.appendChild(textDiv);

  // Add sources if available
  if (sources && sources.length > 0) {
    const sourcesDiv = document.createElement("div");
    sourcesDiv.className = "message-sources";
    sourcesDiv.innerHTML = "<strong>Sources:</strong>";

    sources.forEach((source) => {
      const sourceTag = document.createElement("span");
      sourceTag.className = "source-tag";
      sourceTag.textContent = source;
      sourcesDiv.appendChild(sourceTag);
    });

    content.appendChild(sourcesDiv);
  }

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(content);

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

// Add typing indicator
function addTypingIndicator() {
  if (!chatMessages) return null;
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot-message";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect width="24" height="24" rx="6" fill="url(#botGradientTyping)"/>
            <path d="M6 12L9 9L12 12L15 9L18 12" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
                <linearGradient id="botGradientTyping" x1="0" y1="0" x2="24" y2="24">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
            </defs>
        </svg>
    `;

  const content = document.createElement("div");
  content.className = "message-content";

  const textDiv = document.createElement("div");
  textDiv.className = "message-text";

  const typingDiv = document.createElement("div");
  typingDiv.className = "typing-indicator";
  typingDiv.innerHTML = "<span></span><span></span><span></span>";

  textDiv.appendChild(typingDiv);
  content.appendChild(textDiv);
  messageDiv.appendChild(avatar);
  messageDiv.appendChild(content);

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
