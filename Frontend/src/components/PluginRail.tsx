"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";

export default function PluginRail() {
    const { plugins, activePlugin, switchPlugin } = usePlugin();
    const [collapsed, setCollapsed] = useState(false);

    return (
        <motion.div
            animate={{ width: collapsed ? 68 : 280 }}
            transition={{ duration: 0.25, ease: [0.25, 0.1, 0.25, 1] }}
            className="relative flex-shrink-0 h-full bg-brand-surface border-r border-white/[0.04] flex flex-col overflow-hidden"
        >
            {/* Header */}
            <div className="px-4 pt-4 pb-3 flex items-center justify-between min-h-[52px]">
                <AnimatePresence mode="wait">
                    {!collapsed && (
                        <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.15 }}
                            className="text-white/40 text-[11px] font-semibold uppercase tracking-widest"
                        >
                            Plugins
                        </motion.span>
                    )}
                </AnimatePresence>
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="text-white/30 hover:text-white/60 transition-colors p-1 rounded-md hover:bg-white/5"
                >
                    {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
                </button>
            </div>

            {/* Plugin List */}
            <div className="flex-1 overflow-y-auto px-2 pb-4 space-y-1">
                {plugins.map((plugin) => {
                    const isActive = activePlugin.id === plugin.id;
                    const Icon = plugin.icon;

                    return (
                        <motion.button
                            key={plugin.id}
                            onClick={() => switchPlugin(plugin.id)}
                            whileHover={{ scale: 1.01 }}
                            whileTap={{ scale: 0.98 }}
                            className={`
                relative w-full flex items-center gap-3 rounded-xl transition-all duration-200 group
                ${collapsed ? "justify-center px-0 py-3" : "px-3 py-3"}
                ${isActive
                                    ? "bg-white/[0.06]"
                                    : "hover:bg-white/[0.03]"
                                }
              `}
                        >
                            {/* Active Indicator Glow */}
                            {isActive && (
                                <motion.div
                                    layoutId="activePluginGlow"
                                    className="absolute inset-0 rounded-xl"
                                    style={{
                                        boxShadow: `inset 0 0 20px rgba(${plugin.accentRgb}, 0.08), 0 0 15px rgba(${plugin.accentRgb}, 0.05)`,
                                        border: `1px solid rgba(${plugin.accentRgb}, 0.15)`,
                                    }}
                                    transition={{ duration: 0.25, ease: "easeOut" }}
                                />
                            )}

                            {/* Icon */}
                            <div
                                className="relative z-10 flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-250"
                                style={{
                                    background: isActive
                                        ? `rgba(${plugin.accentRgb}, 0.15)`
                                        : "rgba(255,255,255,0.04)",
                                    color: isActive ? plugin.accent : "rgba(255,255,255,0.4)",
                                }}
                            >
                                <Icon size={18} />
                            </div>

                            {/* Label */}
                            <AnimatePresence mode="wait">
                                {!collapsed && (
                                    <motion.div
                                        initial={{ opacity: 0, x: -8 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -8 }}
                                        transition={{ duration: 0.15 }}
                                        className="relative z-10 flex flex-col items-start min-w-0"
                                    >
                                        <span
                                            className={`text-[13px] font-semibold tracking-tight truncate ${isActive ? "text-white/90" : "text-white/50 group-hover:text-white/70"
                                                }`}
                                        >
                                            {plugin.name}
                                        </span>
                                        <span className="text-[11px] text-white/25 truncate">
                                            {plugin.persona}
                                        </span>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.button>
                    );
                })}
            </div>

            {/* Bottom Accent Line */}
            <div className="h-[2px] mx-4 mb-4 rounded-full overflow-hidden bg-white/[0.03]">
                <motion.div
                    className="h-full rounded-full"
                    style={{ background: activePlugin.accent }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                />
            </div>
        </motion.div>
    );
}
