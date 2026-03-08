"use client";

import { useState, FormEvent, KeyboardEvent } from "react";
import { usePlugin } from "@/context/PluginContext";
import { Send } from "lucide-react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
    const { activePlugin } = usePlugin();
    const [value, setValue] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (!value.trim()) return;
        onSend(value.trim());
        setValue("");
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!value.trim()) return;
            onSend(value.trim());
            setValue("");
        }
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
                    onKeyDown={handleKeyDown}
                    placeholder={`Ask your ${activePlugin.persona}...`}
                    disabled={disabled}
                    className="flex-1 bg-transparent px-5 py-4 text-[14px] text-white/80 placeholder:text-white/25 outline-none disabled:opacity-50"
                />
                <button
                    type="submit"
                    disabled={!value.trim() || disabled}
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
