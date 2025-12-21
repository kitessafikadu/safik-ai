import Link from "next/link";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <div className="">
              <span className="text-white">Safik AI</span>
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
