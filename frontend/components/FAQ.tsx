export default function FAQ() {
  return (
    <section id="faq" className="faq">
      <div className="container">
        <div className="section-header">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <p className="section-subtitle">
            Everything you need to know about our AI services
          </p>
        </div>
        <div className="faq-grid">
          <div className="faq-item">
            <h3>How long does implementation take?</h3>
            <p>
              Implementation timelines vary based on complexity. Basic chatbots
              take 4-6 weeks, while comprehensive AI solutions take 3-6 months.
              You&apos;ll see working prototypes within 2-3 weeks.
            </p>
          </div>
          <div className="faq-item">
            <h3>What industries do you specialize in?</h3>
            <p>
              We have deep expertise in healthcare, financial services, retail,
              manufacturing, and technology. Our methodologies are
              industry-agnostic and we&apos;ve delivered projects across 15+ sectors.
            </p>
          </div>
          <div className="faq-item">
            <h3>How do you ensure data privacy?</h3>
            <p>
              We&apos;re SOC 2 Type II certified, GDPR compliant, and HIPAA
              compliant. All solutions use end-to-end encryption, role-based
              access control, and can be deployed entirely within your
              infrastructure.
            </p>
          </div>
          <div className="faq-item">
            <h3>What support do you provide?</h3>
            <p>
              We offer 24/7 monitoring, incident response, regular model
              retraining, and performance optimization. Our packages include
              training for your team and continuous improvement recommendations.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
