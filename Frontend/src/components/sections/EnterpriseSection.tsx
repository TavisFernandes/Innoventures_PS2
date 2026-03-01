"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { Palette, MessageSquare, Lock, Sliders, Zap, Globe } from "lucide-react";

const FEATURES = [
    {
        icon: MessageSquare,
        title: "Custom System Prompts",
        desc: "Define the AI's persona, expertise area, tone, and behavioral guidelines.",
    },
    {
        icon: Palette,
        title: "Brand Theming",
        desc: "Set accent colors, icons, and visual identity for each plugin.",
    },
    {
        icon: Lock,
        title: "Guardrails & Safety",
        desc: "Configure domain-specific boundaries and ethical constraints.",
    },
    {
        icon: Sliders,
        title: "Knowledge Injection",
        desc: "Upload proprietary docs and data to fine-tune the plugin's responses.",
    },
    {
        icon: Zap,
        title: "Instant Deploy",
        desc: "Go from configuration to production-ready in minutes, not weeks.",
    },
    {
        icon: Globe,
        title: "Multi-Language",
        desc: "Deploy plugins that operate fluently in over 50 languages.",
    },
];

export default function EnterpriseSection() {
    const ref = useRef<HTMLDivElement>(null);
    const isInView = useInView(ref, { once: true, margin: "-100px" });
    const { activePlugin } = usePlugin();

    return (
        <section ref={ref} className="relative py-32 px-6 overflow-hidden">
            <div
                className="absolute inset-0 pointer-events-none"
                style={{
                    background: `radial-gradient(ellipse 800px 500px at 50% 60%, rgba(${activePlugin.accentRgb}, 0.03) 0%, transparent 70%)`,
                }}
            />

            <div className="max-w-[1200px] mx-auto relative z-10">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.7 }}
                    className="text-center max-w-2xl mx-auto mb-16 p-8 md:p-12 rounded-[2rem] bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl"
                >
                    <span
                        className="text-[12px] font-semibold uppercase tracking-widest mb-4 block"
                        style={{ color: activePlugin.accent }}
                    >
                        Enterprise Ready
                    </span>
                    <h2 className="text-white/90 text-3xl md:text-4xl font-bold tracking-tighter leading-tight mb-4">
                        Build your own expert.
                        <br />
                        <span className="gradient-text-subtle">Deploy in minutes.</span>
                    </h2>
                    <p className="text-white/30 text-[15px] leading-relaxed">
                        Define custom system prompts, inject proprietary knowledge, set tone
                        and guardrails. Your SME plugin, your rules.
                    </p>
                </motion.div>

                {/* Feature Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {FEATURES.map((feature, i) => {
                        const Icon = feature.icon;
                        return (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 24 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{
                                    duration: 0.5,
                                    delay: 0.1 + i * 0.08,
                                    ease: [0.25, 0.1, 0.25, 1],
                                }}
                                className="p-6 rounded-2xl bg-black/50 backdrop-blur-xl border border-white/[0.1] hover:bg-black/60 hover:backdrop-blur-2xl hover:border-white/[0.15] transition-all duration-250 group overflow-hidden"
                            >
                                <div
                                    className="w-10 h-10 rounded-xl flex items-center justify-center mb-4 transition-all duration-250"
                                    style={{
                                        background: `rgba(${activePlugin.accentRgb}, 0.08)`,
                                        color: activePlugin.accent,
                                    }}
                                >
                                    <Icon size={20} />
                                </div>
                                <h3 className="text-white/70 text-[14px] font-semibold tracking-tight mb-2 group-hover:text-white/90 transition-colors">
                                    {feature.title}
                                </h3>
                                <p className="text-white/25 text-[13px] leading-relaxed">
                                    {feature.desc}
                                </p>
                            </motion.div>
                        );
                    })}
                </div>

                {/* Enterprise Quote */}
                <motion.p
                    initial={{ opacity: 0, y: 16 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6, delay: 0.7 }}
                    className="text-center text-white/50 text-sm mt-12 max-w-lg mx-auto p-4 rounded-xl bg-black/40 backdrop-blur-lg border border-white/10"
                >
                    From internal HR bots to client-facing legal assistants — PlugMind
                    scales to every use case.
                </motion.p>
            </div>
        </section>
    );
}
