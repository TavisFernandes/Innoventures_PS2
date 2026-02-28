"use client";

import { motion } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { Bot, User } from "lucide-react";

interface MessageBubbleProps {
    message: string;
    sender: "user" | "ai";
    index: number;
}

export default function MessageBubble({ message, sender, index }: MessageBubbleProps) {
    const { activePlugin } = usePlugin();
    const isAI = sender === "ai";

    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: index * 0.08, ease: [0.25, 0.1, 0.25, 1] }}
            className={`flex gap-3 ${isAI ? "justify-start" : "justify-end"}`}
        >
            {isAI && (
                <div
                    className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-1"
                    style={{
                        background: `rgba(${activePlugin.accentRgb}, 0.12)`,
                        color: activePlugin.accent,
                    }}
                >
                    <Bot size={16} />
                </div>
            )}

            <div
                className={`
          max-w-[75%] rounded-2xl px-4 py-3 text-[14px] leading-relaxed
          ${isAI
                        ? "bg-white/[0.04] text-white/70 border-l-[3px]"
                        : "bg-white/[0.08] text-white/80"
                    }
        `}
                style={
                    isAI
                        ? { borderLeftColor: activePlugin.accent }
                        : undefined
                }
            >
                {message}
            </div>

            {!isAI && (
                <div className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-1 bg-white/[0.06] text-white/40">
                    <User size={16} />
                </div>
            )}
        </motion.div>
    );
}
