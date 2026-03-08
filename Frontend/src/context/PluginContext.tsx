"use client";

import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import { Plugin, PLUGINS, getPluginById } from "@/lib/plugins";

interface PluginContextType {
    activePlugin: Plugin;
    switchPlugin: (id: string) => void;
    plugins: Plugin[];
    isTransitioning: boolean;
}

const PluginContext = createContext<PluginContextType | null>(null);

export function PluginProvider({ children }: { children: React.ReactNode }) {
    const [activePlugin, setActivePlugin] = useState<Plugin>(PLUGINS[0]);
    const [isTransitioning, setIsTransitioning] = useState(false);

    const updateCssVars = useCallback((plugin: Plugin) => {
        if (typeof window === 'undefined') return;
        const root = document.documentElement;
        root.style.setProperty("--plugin-accent", plugin.accent);
        root.style.setProperty("--plugin-accent-rgb", plugin.accentRgb);
        root.style.setProperty("--plugin-accent-dim", plugin.accentDim);
    }, []);

    useEffect(() => {
        updateCssVars(activePlugin);
    }, [activePlugin, updateCssVars]);

    const switchPlugin = useCallback(
        (id: string) => {
            if (id === activePlugin.id) return;
            setIsTransitioning(true);
            const newPlugin = getPluginById(id);
            // Rapid transition — update CSS vars immediately for 300ms swap feel
            updateCssVars(newPlugin);
            // Small delay to let AnimatePresence orchestrate
            requestAnimationFrame(() => {
                setActivePlugin(newPlugin);
                setTimeout(() => setIsTransitioning(false), 300);
            });
        },
        [activePlugin.id, updateCssVars]
    );

    return (
        <PluginContext.Provider
            value={{ activePlugin, switchPlugin, plugins: PLUGINS, isTransitioning }}
        >
            {children}
        </PluginContext.Provider>
    );
}

export function usePlugin() {
    const context = useContext(PluginContext);
    // Return default values during SSR
    if (!context) {
        return {
            activePlugin: PLUGINS[0],
            switchPlugin: () => {},
            plugins: PLUGINS,
            isTransitioning: false
        };
    }
    return context;
}
