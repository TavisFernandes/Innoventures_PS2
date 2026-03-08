"use client";

import { usePlugin } from "@/context/PluginContext";
import PluginRail from "./PluginRail";
import ChatPanel from "./ChatPanel";

export default function ChatDemo() {
    const { activePlugin } = usePlugin();

    return (
        <div
            id="chat"
            className="w-full max-w-[1200px] mx-auto rounded-2xl overflow-hidden border border-white/[0.06] bg-brand-bg"
            style={{
                boxShadow: `0 0 80px rgba(${activePlugin.accentRgb}, 0.04), 0 20px 60px rgba(0,0,0,0.5)`,
            }}
        >
            <div className="flex h-full">
                <ChatPanel />
            </div>
        </div>
    );
}
