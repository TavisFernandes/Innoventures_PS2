'use client';

import { PluginProvider } from "@/context/PluginContext";
import { AuthProvider } from "@/context/AuthContext";

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <AuthProvider>
            <PluginProvider>{children}</PluginProvider>
        </AuthProvider>
    );
}
