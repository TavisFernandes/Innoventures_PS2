"use client";

import { useAuth } from '@/context/AuthContext';
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/sections/HeroSection";
import ChatDemo from "@/components/ChatDemo";
import PluginRevealSection from "@/components/sections/PluginRevealSection";
import PersonasSection from "@/components/sections/PersonasSection";
import EnterpriseSection from "@/components/sections/EnterpriseSection";
import CtaSection from "@/components/sections/CtaSection";
import BrainSequence from "@/components/BrainSequence";

export default function Home() {
  const { user } = useAuth();

  return (
    <main className="min-h-screen relative">
      <BrainSequence />
      <Navbar />

      {/* Hero / Intro */}
      <HeroSection />

      {/* Interactive Chat Demo */}
      <section className="relative py-16 px-6">
        <ChatDemo />
      </section>

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
