export default function Services() {
  return (
    <section id="services" className="services">
      <div className="container">
        <div className="section-header">
          <h2 className="section-title">Our Services</h2>
          <p className="section-subtitle">
            Comprehensive AI solutions tailored to your business needs
          </p>
        </div>
        <div className="services-grid">
          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <path
                  d="M24 16V32M16 24H32"
                  stroke="#2563EB"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <h3>RAG Systems</h3>
            <p>
              Build intelligent chatbots and knowledge systems with
              Retrieval-Augmented Generation technology.
            </p>
            <ul className="service-features">
              <li>Real-time document retrieval</li>
              <li>Multi-source integration</li>
              <li>Semantic search capabilities</li>
            </ul>
          </div>

          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <circle
                  cx="24"
                  cy="24"
                  r="8"
                  stroke="#2563EB"
                  strokeWidth="2"
                />
                <path
                  d="M24 16V12M24 36V32M32 24H36M12 24H16"
                  stroke="#2563EB"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <h3>Conversational AI</h3>
            <p>
              Deploy enterprise chatbots for customer service, support, and
              sales enablement across multiple channels.
            </p>
            <ul className="service-features">
              <li>Natural language understanding</li>
              <li>Multi-turn conversations</li>
              <li>24/7 automated support</li>
            </ul>
          </div>

          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <path
                  d="M16 28L20 24L24 28L32 20"
                  stroke="#2563EB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <h3>Custom ML Models</h3>
            <p>
              Develop bespoke machine learning models for predictive analytics,
              forecasting, and automation.
            </p>
            <ul className="service-features">
              <li>Predictive analytics</li>
              <li>Computer vision solutions</li>
              <li>Anomaly detection</li>
            </ul>
          </div>

          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <path
                  d="M20 24L24 28L32 20"
                  stroke="#2563EB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <h3>AI Strategy Consulting</h3>
            <p>
              Expert guidance on AI roadmaps, use case identification, and
              building internal capabilities.
            </p>
            <ul className="service-features">
              <li>AI readiness assessment</li>
              <li>Use case prioritization</li>
              <li>Team training & upskilling</li>
            </ul>
          </div>

          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <rect
                  x="18"
                  y="18"
                  width="12"
                  height="12"
                  rx="2"
                  stroke="#2563EB"
                  strokeWidth="2"
                />
              </svg>
            </div>
            <h3>Model Fine-tuning</h3>
            <p>
              Optimize large language models and foundation models on your
              domain-specific data.
            </p>
            <ul className="service-features">
              <li>Domain-specific training</li>
              <li>Prompt engineering</li>
              <li>Performance optimization</li>
            </ul>
          </div>

          <div className="service-card">
            <div className="service-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect
                  width="48"
                  height="48"
                  rx="12"
                  fill="#2563EB"
                  opacity="0.08"
                />
                <path
                  d="M16 24H32M24 16V32"
                  stroke="#2563EB"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <h3>Vector Database</h3>
            <p>
              Implement and optimize vector databases for semantic search and
              similarity matching.
            </p>
            <ul className="service-features">
              <li>ChromaDB Vector Search</li>
              <li>Embedding optimization</li>
              <li>Hybrid search implementation</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
