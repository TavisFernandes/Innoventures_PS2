import HeroSection from "@/components/sections/HeroSection";
import PluginRevealSection from "@/components/sections/PluginRevealSection";
import PersonasSection from "@/components/sections/PersonasSection";
import EnterpriseSection from "@/components/sections/EnterpriseSection";
import CtaSection from "@/components/sections/CtaSection";
import BrainSequence from "@/components/BrainSequence";

export default function Home() {
  return (
    <main className="min-h-screen relative">
      <BrainSequence />

      {/* Hero / Intro */}
      <HeroSection />

      {/* Plugin Reveal */}
      <PluginRevealSection />

      {/* SME Personas & Intelligence */}
      <PersonasSection />

      {/* Enterprise & Customization */}
      <EnterpriseSection />

      {/* CTA & Closing */}
      <CtaSection />
    </main>
  );
}
