"use client";

import { motion } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";

export default function TypingIndicator() {
    const { activePlugin } = usePlugin();

    return (
        <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="flex items-center gap-3"
        >
            <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{
                    background: `rgba(${activePlugin.accentRgb}, 0.12)`,
                }}
            >
                <div className="flex gap-1">
                    <span
                        className="typing-dot w-1.5 h-1.5 rounded-full"
                        style={{ background: activePlugin.accent }}
                    />
                    <span
                        className="typing-dot w-1.5 h-1.5 rounded-full"
                        style={{ background: activePlugin.accent }}
                    />
                    <span
                        className="typing-dot w-1.5 h-1.5 rounded-full"
                        style={{ background: activePlugin.accent }}
                    />
                </div>
            </div>
            <span className="text-white/25 text-[12px] font-medium">
                {activePlugin.persona} is thinking…
            </span>
        </motion.div>
    );
}
