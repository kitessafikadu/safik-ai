import Link from "next/link";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="logo">
              <svg
                width="32"
                height="32"
                viewBox="0 0 32 32"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect width="32" height="32" rx="6" fill="url(#gradient2)" />
                <path
                  d="M8 16L12 12L16 16L20 12L24 16"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <circle cx="12" cy="12" r="1.5" fill="white" />
                <circle cx="16" cy="16" r="1.5" fill="white" />
                <circle cx="20" cy="12" r="1.5" fill="white" />
                <defs>
                  <linearGradient id="gradient2" x1="0" y1="0" x2="32" y2="32">
                    <stop offset="0%" stopColor="#667eea" />
                    <stop offset="100%" stopColor="#764ba2" />
                  </linearGradient>
                </defs>
              </svg>
              <span>Safik AI</span>
            </div>
            <p className="footer-description">
              Enterprise-grade AI solutions that drive measurable business
              outcomes.
            </p>
          </div>
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li>
                <Link href="/#about">About Us</Link>
              </li>
              <li>
                <Link href="/#services">Services</Link>
              </li>
              <li>
                <Link href="/chatbot">AI Chatbot</Link>
              </li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li>
                <Link href="/#faq">FAQ</Link>
              </li>
              <li>
                <a href="#">Documentation</a>
              </li>
              <li>
                <a href="#">Contact</a>
              </li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 Safik AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
