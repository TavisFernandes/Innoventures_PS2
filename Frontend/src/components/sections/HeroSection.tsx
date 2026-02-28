"use client";

import { motion } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { Sparkles } from "lucide-react";

export default function HeroSection() {
    const { activePlugin } = usePlugin();

    return (
        <section className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
            {/* Ambient Background Glow */}
            <div
                className="absolute inset-0 pointer-events-none"
                style={{
                    background: `radial-gradient(ellipse 600px 400px at 50% 40%, rgba(${activePlugin.accentRgb}, 0.06) 0%, transparent 70%)`,
                }}
            />

            {/* Glass Content Card */}
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="relative z-10 flex flex-col items-center justify-center p-8 md:p-12 rounded-[2rem] bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl max-w-3xl w-full"
            >
                {/* Top Badge */}
                <motion.div
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="mb-8 flex items-center gap-2 px-4 py-2 rounded-full bg-white/[0.04] border border-white/[0.06]"
                >
                    <Sparkles size={14} style={{ color: activePlugin.accent }} />
                    <span className="text-white/50 text-[12px] font-medium tracking-wide">
                        AI-POWERED EXPERT SYSTEM
                    </span>
                </motion.div>

                {/* Main Headline */}
                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7, delay: 0.3 }}
                    className="gradient-text-subtle text-center font-bold tracking-tighter leading-[0.95] pb-2 md:pb-4"
                    style={{ fontSize: "clamp(48px, 8vw, 96px)" }}
                >
                    PlugMind
                </motion.h1>

                {/* Subtitle */}
                <motion.p
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.5 }}
                    className="mt-5 text-white/50 text-center text-lg md:text-xl font-medium tracking-tight max-w-xl"
                >
                    One chatbot. Every expert.
                </motion.p>

                {/* Supporting Line */}
                <motion.p
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.65 }}
                    className="mt-3 text-white/30 text-center text-sm md:text-[15px] max-w-lg leading-relaxed"
                >
                    Hot-swap subject matter expert plugins instantly — legal, medical,
                    financial, technical — no reloads, no friction.
                </motion.p>

                {/* CTA Buttons */}
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                    className="mt-8 flex items-center gap-4"
                >
                    <a href="#chat" className="btn-gradient text-sm">
                        Start for Free
                    </a>
                    <a href="#plugins" className="btn-outline text-sm">
                        Explore Plugins
                    </a>
                </motion.div>
            </motion.div>

            {/* Scroll Indicator */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.5, duration: 1 }}
                className="absolute bottom-10 flex flex-col items-center gap-2"
            >
                <span className="text-white/20 text-[11px] font-medium tracking-wider uppercase">
                    Scroll to explore
                </span>
                <motion.div
                    animate={{ y: [0, 6, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                    className="w-5 h-8 rounded-full border border-white/10 flex items-start justify-center pt-1.5"
                >
                    <div
                        className="w-1 h-2 rounded-full"
                        style={{ background: activePlugin.accent }}
                    />
                </motion.div>
            </motion.div>
        </section>
    );
}
