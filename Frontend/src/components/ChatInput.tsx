"use client";

import { useState, FormEvent } from "react";
import { usePlugin } from "@/context/PluginContext";
import { Send } from "lucide-react";

interface ChatInputProps {
    onSend: (message: string) => void;
}

export default function ChatInput({ onSend }: ChatInputProps) {
    const { activePlugin } = usePlugin();
    const [value, setValue] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (!value.trim()) return;
        onSend(value.trim());
        setValue("");
    };

    return (
        <form onSubmit={handleSubmit} className="relative">
            <div className="relative flex items-center bg-white/[0.04] border border-white/[0.06] rounded-2xl overflow-hidden transition-all duration-200 focus-within:border-white/[0.12] focus-within:bg-white/[0.05]"
                style={{
                    boxShadow: value
                        ? `0 0 20px rgba(${activePlugin.accentRgb}, 0.06)`
                        : "none",
                }}
            >
                <input
                    type="text"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder={`Ask your ${activePlugin.persona}...`}
                    className="flex-1 bg-transparent px-5 py-4 text-[14px] text-white/80 placeholder:text-white/25 outline-none"
                />
                <button
                    type="submit"
                    disabled={!value.trim()}
                    className="flex-shrink-0 mr-2 w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
                    style={{
                        background: value.trim()
                            ? `rgba(${activePlugin.accentRgb}, 0.15)`
                            : "transparent",
                        color: value.trim() ? activePlugin.accent : "rgba(255,255,255,0.2)",
                    }}
                >
                    <Send size={16} />
                </button>
            </div>
        </form>
    );
}
