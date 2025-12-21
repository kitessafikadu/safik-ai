import Hero from "@/components/Hero";
import Services from "@/components/Services";
import About from "@/components/About";
import FAQ from "@/components/FAQ";
import CTA from "@/components/CTA";

export default function Home() {
  return (
    <main>
      <Hero />
      <Services />
      <About />
      <FAQ />
      <CTA />
    </main>
  );
}
