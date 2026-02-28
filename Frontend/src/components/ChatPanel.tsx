"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import SuggestedPrompts from "./SuggestedPrompts";
import TypingIndicator from "./TypingIndicator";

interface Message {
    id: string;
    text: string;
    sender: "user" | "ai";
}

// Simulated AI responses per plugin
const AI_RESPONSES: Record<string, string[]> = {
    default: [
        "I'd be happy to help with that. Could you provide more details so I can give you a thorough response?",
        "Great question! Let me break this down for you in a clear, structured way.",
        "I've analyzed your request. Here's what I recommend based on best practices.",
    ],
    legal: [
        "Based on my analysis, there are several contractual provisions to consider here. Please note this does not constitute legal advice.",
        "From a compliance perspective, this falls under the jurisdiction of the relevant regulatory framework. I'd recommend consulting with your legal counsel.",
        "I've identified three potential risk areas in this agreement. Let me walk you through each one.",
    ],
    medical: [
        "Based on current clinical evidence, here's what the research suggests. Please consult your healthcare provider for personalized guidance.",
        "This is a common clinical scenario. The standard approach generally involves the following considerations.",
        "I've reviewed the relevant literature. Here's a summary of the key findings and their clinical implications.",
    ],
    finance: [
        "Looking at the fundamentals, there are several key metrics to evaluate here. Remember, this is informational, not investment advice.",
        "From a portfolio allocation perspective, diversification across these asset classes could help manage risk exposure.",
        "The current market conditions suggest several strategic considerations. Let me outline the key factors.",
    ],
    engineering: [
        "From an architectural standpoint, I'd recommend considering a modular approach here. Let me outline the tradeoffs.",
        "Looking at this from a systems design perspective, there are some scalability considerations worth addressing.",
        "I've identified a potential optimization path. Here's the approach I'd recommend with the relevant technical context.",
    ],
    hr: [
        "Based on HR best practices, here's a comprehensive approach to address this situation effectively.",
        "From a talent management perspective, I'd recommend focusing on these key engagement drivers.",
        "This aligns with modern workforce analytics. Let me outline a data-driven approach to this challenge.",
    ],
    cybersecurity: [
        "I've assessed the threat landscape for this scenario. Here are the critical vulnerabilities to address immediately.",
        "From a security posture perspective, implementing a defense-in-depth strategy would be advisable here.",
        "Based on the MITRE ATT&CK framework, here are the potential attack vectors and recommended mitigations.",
    ],
};

export default function ChatPanel() {
    const { activePlugin } = usePlugin();
    const [messages, setMessages] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const prevPluginRef = useRef(activePlugin.id);

    const scrollToBottom = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages, scrollToBottom]);

    // Add welcome message when plugin changes
    useEffect(() => {
        if (prevPluginRef.current !== activePlugin.id) {
            prevPluginRef.current = activePlugin.id;
            const welcomeMsg: Message = {
                id: `welcome-${activePlugin.id}-${Date.now()}`,
                text: `${activePlugin.persona} activated. I specialize in ${activePlugin.description.toLowerCase()}. How can I assist you today?`,
                sender: "ai",
            };
            setMessages((prev) => [...prev, welcomeMsg]);
        }
    }, [activePlugin]);

    const handleSend = (text: string) => {
        const userMsg: Message = {
            id: `user-${Date.now()}`,
            text,
            sender: "user",
        };
        setMessages((prev) => [...prev, userMsg]);
        setIsTyping(true);

        // Simulate AI response
        const responses = AI_RESPONSES[activePlugin.id] || AI_RESPONSES.default;
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        setTimeout(() => {
            setIsTyping(false);
            const aiMsg: Message = {
                id: `ai-${Date.now()}`,
                text: randomResponse,
                sender: "ai",
            };
            setMessages((prev) => [...prev, aiMsg]);
        }, 1200 + Math.random() * 800);
    };

    return (
        <div className="flex-1 flex flex-col h-full min-w-0">
            {/* Persona Header */}
            <div className="flex-shrink-0 px-6 py-4 border-b border-white/[0.04] flex items-center gap-3">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={activePlugin.id}
                        initial={{ opacity: 0, y: -8 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 8 }}
                        transition={{ duration: 0.2 }}
                        className="flex items-center gap-3"
                    >
                        <div
                            className="w-2 h-2 rounded-full"
                            style={{ background: activePlugin.accent, boxShadow: `0 0 8px ${activePlugin.accent}` }}
                        />
                        <span className="text-white/80 text-[14px] font-semibold tracking-tight">
                            {activePlugin.persona}
                        </span>
                        <span className="text-white/20 text-[12px] font-medium px-2 py-0.5 rounded-md bg-white/[0.03]">
                            Active
                        </span>
                    </motion.div>
                </AnimatePresence>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-center">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.5 }}
                            className="mb-6"
                        >
                            <div
                                className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4"
                                style={{ background: `rgba(${activePlugin.accentRgb}, 0.1)` }}
                            >
                                {(() => {
                                    const Icon = activePlugin.icon;
                                    return <Icon size={28} style={{ color: activePlugin.accent }} />;
                                })()}
                            </div>
                            <h3 className="text-white/70 text-lg font-semibold tracking-tight mb-2">
                                {activePlugin.persona}
                            </h3>
                            <p className="text-white/30 text-sm max-w-sm">
                                {activePlugin.description}. Select a prompt below or type your own question.
                            </p>
                        </motion.div>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <MessageBubble key={msg.id} message={msg.text} sender={msg.sender} index={i} />
                ))}

                <AnimatePresence>
                    {isTyping && <TypingIndicator />}
                </AnimatePresence>

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="flex-shrink-0 px-6 pb-4 pt-2 space-y-3 border-t border-white/[0.04]">
                <SuggestedPrompts onSelect={handleSend} />
                <ChatInput onSend={handleSend} />
            </div>
        </div>
    );
}
