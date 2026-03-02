"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { apiService, ChatMessage } from "@/lib/api";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import SuggestedPrompts from "./SuggestedPrompts";
import FileUploadComponent from "./FileUpload";
import { FileUpload } from "@/lib/fileUpload";

export default function ChatPanel() {
    const { activePlugin, switchPlugin, plugins } = usePlugin();
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [uploadedFiles, setUploadedFiles] = useState<FileUpload[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const prevPluginRef = useRef(activePlugin.id);

    const scrollToBottom = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, []);

    const scrollToBottomInstant = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "instant" });
    }, []);

    // Removed auto-scroll on every message change to prevent automatic dragging
    // Users can now scroll freely through chat history

    // Check API connection on mount
    useEffect(() => {
        const checkConnection = async () => {
            try {
                const isHealthy = await apiService.healthCheck();
                setIsConnected(isHealthy);
                if (!isHealthy) {
                    setError("Unable to connect to backend. Please ensure the backend server is running on localhost:8001");
                }
            } catch (err) {
                setError("Backend connection failed. Please try again later.");
            }
        };
        checkConnection();
    }, []);

    // Add welcome message when plugin changes
    useEffect(() => {
        if (prevPluginRef.current !== activePlugin.id) {
            prevPluginRef.current = activePlugin.id;
            const welcomeMsg: ChatMessage = {
                id: `welcome-${activePlugin.id}-${Date.now()}`,
                text: `${activePlugin.persona} activated. I specialize in ${activePlugin.description.toLowerCase()}. How can I assist you today?`,
                sender: "ai",
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, welcomeMsg]);

            // Scroll to bottom when welcome message appears
            setTimeout(() => scrollToBottom(), 100);
        }
    }, [activePlugin, scrollToBottom]);

    const handleSend = async (text: string) => {
        if (!isConnected) {
            setError("Cannot send message. Backend is not connected.");
            return;
        }

        const userMsg: ChatMessage = {
            id: `user-${Date.now()}`,
            text,
            sender: "user",
            timestamp: new Date(),
            files: uploadedFiles.length > 0 ? uploadedFiles : undefined
        };
        setMessages((prev) => [...prev, userMsg]);
        setIsTyping(true);
        setError(null);

        // Scroll to bottom when response arrives
        setTimeout(() => scrollToBottom(), 100);

        try {
            let response;

            // Use multi-modal messaging if files are uploaded
            if (uploadedFiles.length > 0) {
                response = await apiService.sendMultiModalMessage(text, uploadedFiles);
            } else {
                response = await apiService.sendMessage(text);
            }

            setIsTyping(false);

            const aiMsg: ChatMessage = {
                id: `ai-${Date.now()}`,
                text: response.answer,
                sender: "ai",
                timestamp: new Date(),
                domain: response.domain,
                confidence: response.confidence,
                sources: response.sources,
                methodology: response.methodology,
                citations: response.citations,
                disclaimer: response.disclaimer,
                multimodal_analysis: response.multimodal_analysis
            };

            setMessages((prev) => [...prev, aiMsg]);

            if (response.domain) {
                const matched = plugins.find(p =>
                    p.id.toLowerCase() === response.domain.toLowerCase() ||
                    p.name.toLowerCase() === response.domain.toLowerCase() ||
                    p.persona.toLowerCase() === response.domain.toLowerCase()
                );
                if (matched && matched.id !== activePlugin.id) {
                    switchPlugin(matched.id);
                }
            }

            // Clear uploaded files after sending
            setUploadedFiles([]);

            // Scroll to bottom when response arrives
            setTimeout(() => scrollToBottom(), 100);
        } catch (err) {
            setIsTyping(false);
            setError("Failed to get response from backend. Please try again.");

            // Add error message
            const errorMsg: ChatMessage = {
                id: `error-${Date.now()}`,
                text: "I apologize, but I'm having trouble connecting to the backend right now. Please ensure the backend server is running on localhost:8001.",
                sender: "ai",
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMsg]);

            // Scroll to bottom when error message arrives
            setTimeout(() => scrollToBottom(), 100);
        }
    };

    const handleFilesSelected = (files: FileUpload[]) => {
        setUploadedFiles(files);
    };

    return (
        <div className="flex-1 flex flex-col h-full min-w-0">
            {/* Connection Status */}
            <div className="flex-shrink-0 px-6 py-2 border-b border-white/[0.04] flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div
                        className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}
                    />
                    <span className="text-white/70 text-sm font-medium">
                        {isConnected ? 'Backend Connected' : 'Backend Disconnected'}
                    </span>
                </div>
                <div className="flex items-center gap-4">
                    <span className="text-white/50 text-xs">
                        Domain: <span className="text-white/70 font-medium">{activePlugin.persona}</span>
                    </span>
                    <span className="text-white/30 text-xs">
                        {activePlugin.description}
                    </span>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="flex-shrink-0 mx-6 mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                    <p className="text-red-400 text-sm">{error}</p>
                </div>
            )}

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
                            {!isConnected && (
                                <p className="text-yellow-400 text-sm max-w-sm mt-4">
                                    ⚠️ Backend server is not running. Please start the backend to enable chat functionality.
                                </p>
                            )}
                        </motion.div>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <MessageBubble
                        key={msg.id}
                        message={msg.text}
                        sender={msg.sender}
                        index={i}
                        domain={msg.domain}
                        confidence={msg.confidence}
                        sources={msg.sources}
                        methodology={msg.methodology}
                        citations={msg.citations}
                        disclaimer={msg.disclaimer}
                        files={msg.files}
                        multimodalAnalysis={msg.multimodal_analysis}
                    />
                ))}

                <AnimatePresence>
                    {isTyping && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 10 }}
                            transition={{ duration: 0.3 }}
                        >
                            <TypingIndicator />
                        </motion.div>
                    )}
                </AnimatePresence>

                <div ref={messagesEndRef} className="h-0" />
            </div>

            {/* Input Area */}
            <div className="flex-shrink-0 px-6 pb-4 pt-2 space-y-3 border-t border-white/[0.04]">
                {/* File Upload */}
                <FileUploadComponent
                    onFilesSelected={handleFilesSelected}
                    disabled={!isConnected}
                />

                {/* Uploaded Files Display */}
                {uploadedFiles.length > 0 && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                        <div className="flex items-center justify-between">
                            <span className="text-sm text-blue-700">
                                {uploadedFiles.length} file(s) uploaded
                            </span>
                            <button
                                onClick={() => setUploadedFiles([])}
                                className="text-blue-500 hover:text-blue-700 text-sm"
                            >
                                Clear
                            </button>
                        </div>
                    </div>
                )}

                <ChatInput onSend={handleSend} disabled={!isConnected} />
            </div>
        </div>
    );
}
