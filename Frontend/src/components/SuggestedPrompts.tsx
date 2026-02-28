"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";

export default function SuggestedPrompts({
    onSelect,
}: {
    onSelect: (prompt: string) => void;
}) {
    const { activePlugin } = usePlugin();

    return (
        <div className="flex flex-wrap gap-2">
            <AnimatePresence mode="popLayout">
                {activePlugin.suggestedPrompts.map((prompt, i) => (
                    <motion.button
                        key={`${activePlugin.id}-${i}`}
                        initial={{ opacity: 0, scale: 0.9, y: 6 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: -6 }}
                        transition={{ duration: 0.2, delay: i * 0.04 }}
                        whileHover={{ scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                        onClick={() => onSelect(prompt)}
                        className="px-3.5 py-2 rounded-xl text-[12px] font-medium text-white/50 hover:text-white/80 bg-white/[0.03] hover:bg-white/[0.06] border border-white/[0.06] hover:border-white/[0.1] transition-colors duration-200 flex-shrink-0"
                    >
                        {prompt}
                    </motion.button>
                ))}
            </AnimatePresence>
        </div>
    );
}
