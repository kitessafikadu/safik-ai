export default function About() {
  return (
    <section id="about" className="about">
      <div className="container">
        <div className="about-grid">
          <div className="about-content">
            <h2 className="section-title">About Safik AI</h2>
            <p className="about-text">
              Founded in 2020, Safik AI emerged from a simple observation: while
              AI technology was advancing rapidly, most organizations struggled to
              implement it effectively. Our founders, a team of former Google
              and Microsoft AI researchers, set out to bridge this gap.
            </p>
            <p className="about-text">
              Today, we&apos;re a team of 45 AI specialists serving clients across
              healthcare, finance, retail, and technology sectors. We&apos;ve
              processed over 10 billion data points, deployed 200+ AI models in
              production, and helped our clients achieve an average of 35%
              operational efficiency improvements.
            </p>
            <div className="about-values">
              <div className="value-item">
                <h4>Innovation</h4>
                <p>
                  Staying at the forefront of AI research and translating
                  cutting-edge techniques into practical solutions.
                </p>
              </div>
              <div className="value-item">
                <h4>Integrity</h4>
                <p>
                  Prioritizing ethical AI development, ensuring data privacy,
                  and maintaining transparency.
                </p>
              </div>
              <div className="value-item">
                <h4>Impact</h4>
                <p>
                  Measuring success through tangible business outcomes rather
                  than just technical metrics.
                </p>
              </div>
            </div>
          </div>
          <div className="about-image">
            <div className="stats-card">
              <div className="stats-card-item">
                <div className="stats-number">45</div>
                <div className="stats-text">AI Specialists</div>
              </div>
              <div className="stats-card-item">
                <div className="stats-number">10B+</div>
                <div className="stats-text">Data Points Processed</div>
              </div>
              <div className="stats-card-item">
                <div className="stats-number">35%</div>
                <div className="stats-text">Avg. Efficiency Gain</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
