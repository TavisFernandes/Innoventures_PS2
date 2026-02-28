"use client";

import { useRef, useState, useEffect } from "react";
import { motion, useInView, AnimatePresence } from "framer-motion";
import { PLUGINS } from "@/lib/plugins";
import { usePlugin } from "@/context/PluginContext";
import { ArrowRight } from "lucide-react";

export default function PersonasSection() {
    const ref = useRef<HTMLDivElement>(null);
    const isInView = useInView(ref, { once: true, margin: "-100px" });
    const { activePlugin } = usePlugin();
    const [demoIndex, setDemoIndex] = useState(0);

    // Auto-cycle through plugins for the demo
    useEffect(() => {
        if (!isInView) return;
        const interval = setInterval(() => {
            setDemoIndex((prev) => (prev + 1) % PLUGINS.length);
        }, 3000);
        return () => clearInterval(interval);
    }, [isInView]);

    const demoPlugin = PLUGINS[demoIndex];

    return (
        <section ref={ref} className="relative py-32 px-6 overflow-hidden">
            {/* Background */}
            <div
                className="absolute inset-0 pointer-events-none"
                style={{
                    background: `radial-gradient(ellipse 600px 400px at 70% 50%, rgba(${demoPlugin.accentRgb}, 0.04) 0%, transparent 70%)`,
                }}
            />

            <div className="max-w-[1200px] mx-auto relative z-10">
                <div className="flex flex-col lg:flex-row items-center gap-16">
                    {/* Demo Panel — Left */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        animate={isInView ? { opacity: 1, x: 0 } : {}}
                        transition={{ duration: 0.6 }}
                        className="flex-1 w-full max-w-lg"
                    >
                        <div className="rounded-2xl border border-white/[0.06] bg-brand-surface p-6 overflow-hidden">
                            {/* Persona Badge */}
                            <div className="flex items-center gap-3 mb-6">
                                <AnimatePresence mode="wait">
                                    <motion.div
                                        key={demoPlugin.id}
                                        initial={{ opacity: 0, scale: 0.8 }}
                                        animate={{ opacity: 1, scale: 1 }}
                                        exit={{ opacity: 0, scale: 0.8 }}
                                        transition={{ duration: 0.25 }}
                                        className="flex items-center gap-3"
                                    >
                                        <div
                                            className="w-10 h-10 rounded-xl flex items-center justify-center"
                                            style={{
                                                background: `rgba(${demoPlugin.accentRgb}, 0.15)`,
                                                color: demoPlugin.accent,
                                            }}
                                        >
                                            {(() => {
                                                const Icon = demoPlugin.icon;
                                                return <Icon size={20} />;
                                            })()}
                                        </div>
                                        <div>
                                            <span className="text-white/80 text-[14px] font-semibold block tracking-tight">
                                                {demoPlugin.persona}
                                            </span>
                                            <span className="text-white/25 text-[11px]">
                                                {demoPlugin.name} Plugin
                                            </span>
                                        </div>
                                    </motion.div>
                                </AnimatePresence>
                            </div>

                            {/* Suggested Prompts Demo */}
                            <div className="space-y-2">
                                <span className="text-white/20 text-[11px] font-medium uppercase tracking-wider">
                                    Suggested Prompts
                                </span>
                                <AnimatePresence mode="wait">
                                    <motion.div
                                        key={demoPlugin.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: -10 }}
                                        transition={{ duration: 0.25 }}
                                        className="space-y-2"
                                    >
                                        {demoPlugin.suggestedPrompts.slice(0, 3).map((prompt, i) => (
                                            <div
                                                key={i}
                                                className="flex items-center gap-2 px-3 py-2.5 rounded-xl bg-white/[0.03] border border-white/[0.04]"
                                            >
                                                <ArrowRight
                                                    size={12}
                                                    style={{ color: demoPlugin.accent }}
                                                    className="flex-shrink-0"
                                                />
                                                <span className="text-white/40 text-[13px]">{prompt}</span>
                                            </div>
                                        ))}
                                    </motion.div>
                                </AnimatePresence>
                            </div>

                            {/* Plugin Indicators */}
                            <div className="flex items-center gap-2 mt-6 pt-4 border-t border-white/[0.04]">
                                {PLUGINS.map((p, i) => (
                                    <motion.div
                                        key={p.id}
                                        className="w-2 h-2 rounded-full cursor-pointer"
                                        onClick={() => setDemoIndex(i)}
                                        style={{
                                            background:
                                                i === demoIndex ? demoPlugin.accent : "rgba(255,255,255,0.1)",
                                        }}
                                        animate={{
                                            scale: i === demoIndex ? 1.3 : 1,
                                        }}
                                        transition={{ duration: 0.2 }}
                                    />
                                ))}
                            </div>
                        </div>
                    </motion.div>

                    {/* Copy — Right Aligned */}
                    <motion.div
                        initial={{ opacity: 0, x: 40 }}
                        animate={isInView ? { opacity: 1, x: 0 } : {}}
                        transition={{ duration: 0.7, delay: 0.15 }}
                        className="flex-1 max-w-lg p-8 md:p-10 rounded-[2rem] bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl"
                    >
                        <span
                            className="text-[12px] font-semibold uppercase tracking-widest mb-4 block"
                            style={{ color: activePlugin.accent }}
                        >
                            Deep Specialization
                        </span>
                        <h2 className="text-white/90 text-3xl md:text-4xl font-bold tracking-tighter leading-tight mb-6">
                            Each plugin is a specialist,
                            <br />
                            <span className="gradient-text-subtle">not a generalist.</span>
                        </h2>
                        <div className="space-y-4">
                            {[
                                "Deep domain system prompts trained for precision and safety.",
                                "Context-aware guardrails per plugin — your Medical plugin won't give legal advice.",
                                "Instant hot-swap — your conversation history carries over, your expert changes.",
                            ].map((point, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={isInView ? { opacity: 1, x: 0 } : {}}
                                    transition={{ duration: 0.5, delay: 0.3 + i * 0.1 }}
                                    className="flex items-start gap-3"
                                >
                                    <div
                                        className="w-1.5 h-1.5 rounded-full mt-2 flex-shrink-0"
                                        style={{ background: activePlugin.accent }}
                                    />
                                    <p className="text-white/35 text-[14px] leading-relaxed">
                                        {point}
                                    </p>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
