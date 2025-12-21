import Link from "next/link";

export default function CTA() {
  return (
    <section className="cta">
      <div className="container">
        <div className="cta-content">
          <h2>Ready to Transform Your Business with AI?</h2>
          <p>
            Chat with our AI-powered assistant to learn more about our services
            and solutions.
          </p>
          <Link href="/chatbot" className="btn btn-primary btn-large">
            Start Chatting Now
          </Link>
        </div>
      </div>
    </section>
  );
}
