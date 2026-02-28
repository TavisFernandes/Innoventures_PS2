"use client";

import { useRef } from "react";
import { motion, useInView } from "framer-motion";
import { PLUGINS } from "@/lib/plugins";
import { usePlugin } from "@/context/PluginContext";

export default function PluginRevealSection() {
    const ref = useRef<HTMLDivElement>(null);
    const isInView = useInView(ref, { once: true, margin: "-100px" });
    const { switchPlugin, activePlugin } = usePlugin();

    return (
        <section
            id="plugins"
            ref={ref}
            className="relative py-32 px-6 overflow-hidden"
        >
            {/* Background Gradient */}
            <div
                className="absolute inset-0 pointer-events-none"
                style={{
                    background: `radial-gradient(ellipse 800px 500px at 30% 50%, rgba(${activePlugin.accentRgb}, 0.03) 0%, transparent 70%)`,
                }}
            />

            <div className="max-w-[1200px] mx-auto relative z-10">
                {/* Copy — Left Aligned */}
                <motion.div
                    initial={{ opacity: 0, x: -40 }}
                    animate={isInView ? { opacity: 1, x: 0 } : {}}
                    transition={{ duration: 0.7, ease: [0.25, 0.1, 0.25, 1] }}
                    className="max-w-lg mb-16 p-8 md:p-10 rounded-[2rem] bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl"
                >
                    <span
                        className="text-[12px] font-semibold uppercase tracking-widest mb-4 block"
                        style={{ color: activePlugin.accent }}
                    >
                        Plugin System
                    </span>
                    <h2 className="text-white/90 text-3xl md:text-4xl font-bold tracking-tighter leading-tight mb-4">
                        Plug in any expert.
                        <br />
                        <span className="gradient-text-subtle">In under a second.</span>
                    </h2>
                    <p className="text-white/35 text-[15px] leading-relaxed mb-3">
                        Switch from your Legal Advisor to your Financial Analyst without
                        losing context. Each plugin brings its own persona, knowledge depth,
                        and domain guardrails.
                    </p>
                    <p className="text-white/25 text-[13px] font-medium">
                        Built for teams that can&apos;t afford generic answers.
                    </p>
                </motion.div>

                {/* Plugin Cards Grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {PLUGINS.map((plugin, i) => {
                        const Icon = plugin.icon;
                        const isActive = activePlugin.id === plugin.id;

                        return (
                            <motion.button
                                key={plugin.id}
                                initial={{ opacity: 0, y: 30 }}
                                animate={isInView ? { opacity: 1, y: 0 } : {}}
                                transition={{
                                    duration: 0.5,
                                    delay: 0.2 + i * 0.08,
                                    ease: [0.25, 0.1, 0.25, 1],
                                }}
                                whileHover={{ scale: 1.03, y: -2 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => switchPlugin(plugin.id)}
                                className={`
                  relative text-left p-5 rounded-2xl border transition-all duration-250 group overflow-hidden
                  ${isActive
                                        ? "bg-black/40 backdrop-blur-md border border-white/10"
                                        : "bg-black/20 backdrop-blur-sm border-white/[0.04] hover:bg-black/30 hover:backdrop-blur-md hover:border-white/[0.08]"
                                    }
                `}
                                style={
                                    isActive
                                        ? {
                                            boxShadow: `0 0 30px rgba(${plugin.accentRgb}, 0.08), inset 0 0 20px rgba(${plugin.accentRgb}, 0.04)`,
                                        }
                                        : undefined
                                }
                            >
                                {/* Icon */}
                                <div
                                    className="w-10 h-10 rounded-xl flex items-center justify-center mb-4 transition-all duration-250"
                                    style={{
                                        background: isActive
                                            ? `rgba(${plugin.accentRgb}, 0.15)`
                                            : "rgba(255,255,255,0.04)",
                                        color: isActive ? plugin.accent : "rgba(255,255,255,0.3)",
                                    }}
                                >
                                    <Icon size={20} />
                                </div>

                                {/* Text */}
                                <h3
                                    className={`text-[14px] font-semibold tracking-tight mb-1 transition-colors duration-200 ${isActive
                                        ? "text-white/90"
                                        : "text-white/50 group-hover:text-white/70"
                                        }`}
                                >
                                    {plugin.name}
                                </h3>
                                <p className="text-white/25 text-[12px] leading-relaxed">
                                    {plugin.persona}
                                </p>

                                {/* Active dot */}
                                {isActive && (
                                    <motion.div
                                        layoutId="activePluginDot"
                                        className="absolute top-3 right-3 w-2 h-2 rounded-full"
                                        style={{
                                            background: plugin.accent,
                                            boxShadow: `0 0 8px ${plugin.accent}`,
                                        }}
                                    />
                                )}
                            </motion.button>
                        );
                    })}
                </div>
            </div>
        </section>
    );
}
