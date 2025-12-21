import Link from "next/link";

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-background">
        <div className="hero-gradient"></div>
      </div>
      <div className="container">
        <div className="hero-content">
          <h1 className="hero-title">
            Transform Your Business with
            <span className="gradient-text"> Advanced AI Solutions</span>
          </h1>
          <p className="hero-subtitle">
            Enterprise-grade AI implementations powered by cutting-edge machine
            learning, natural language processing, and intelligent automation.
          </p>
          <div className="hero-buttons">
            <Link href="/chatbot" className="btn btn-primary">
              Try Our AI Chatbot
            </Link>
            <Link href="#services" className="btn btn-secondary">
              Explore Services
            </Link>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <div className="stat-number">200+</div>
              <div className="stat-label">AI Models Deployed</div>
            </div>
            <div className="stat">
              <div className="stat-number">50+</div>
              <div className="stat-label">Enterprise Clients</div>
            </div>
            <div className="stat">
              <div className="stat-number">95%</div>
              <div className="stat-label">Client Retention</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
