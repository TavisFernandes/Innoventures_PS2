"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";

export default function CtaSection() {
    const ref = useRef<HTMLDivElement>(null);
    const isInView = useInView(ref, { once: true, margin: "-80px" });
    const { activePlugin } = usePlugin();

    return (
        <section
            ref={ref}
            className="relative py-32 px-6 overflow-hidden"
        >
            {/* Ambient glow */}
            <div
                className="absolute inset-0 pointer-events-none"
                style={{
                    background: `radial-gradient(ellipse 700px 400px at 50% 60%, rgba(${activePlugin.accentRgb}, 0.06) 0%, transparent 70%)`,
                }}
            />

            <div className="max-w-4xl mx-auto relative z-10 text-center p-8 md:p-16 rounded-[2.5rem] bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl">
                {/* Headline */}
                <motion.h2
                    initial={{ opacity: 0, y: 30 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.7 }}
                    className="text-white/90 text-4xl md:text-5xl lg:text-6xl font-bold tracking-tighter leading-[0.95] mb-4"
                >
                    Ask anything.
                    <br />
                    <span className="gradient-text-subtle">With the right expert.</span>
                </motion.h2>

                {/* Subheadline */}
                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6, delay: 0.15 }}
                    className="text-white/35 text-lg font-medium tracking-tight mb-8"
                >
                    PlugMind. Intelligent, specialized, and always ready.
                </motion.p>

                {/* Buttons */}
                <motion.div
                    initial={{ opacity: 0, y: 16 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="flex items-center justify-center gap-4 mb-8"
                >
                    <a href="#chat" className="btn-gradient text-sm px-8 py-3">
                        Start for Free
                    </a>
                    <a href="#plugins" className="btn-outline text-sm px-8 py-3">
                        Explore All Plugins
                    </a>
                </motion.div>

                {/* Micro-copy */}
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={isInView ? { opacity: 1 } : {}}
                    transition={{ duration: 0.5, delay: 0.5 }}
                    className="text-white/15 text-[13px]"
                >
                    No credit card required · Switch plugins at any time · Built for
                    professionals
                </motion.p>
            </div>

            {/* Footer */}
            <div className="max-w-[1200px] mx-auto mt-24 pt-8 border-t border-white/[0.04] flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                    <div
                        className="w-6 h-6 rounded-md flex items-center justify-center text-white font-bold text-[10px]"
                        style={{ background: activePlugin.accent }}
                    >
                        P
                    </div>
                    <span className="text-white/30 text-[13px] font-medium tracking-tight">
                        PlugMind
                    </span>
                </div>
                <div className="flex items-center gap-6">
                    {["Privacy", "Terms", "Status", "Contact"].map((link) => (
                        <a
                            key={link}
                            href="#"
                            className="text-white/20 hover:text-white/40 text-[12px] transition-colors"
                        >
                            {link}
                        </a>
                    ))}
                </div>
                <span className="text-white/15 text-[12px]">
                    © 2026 PlugMind. All rights reserved.
                </span>
            </div>
        </section>
    );
}
