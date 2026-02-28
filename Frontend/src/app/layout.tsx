import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { PluginProvider } from "@/context/PluginContext";

const inter = Inter({
    subsets: ["latin"],
    variable: "--font-inter",
    display: "swap",
});

export const metadata: Metadata = {
    title: "PlugMind — One Chatbot. Every Expert.",
    description:
        "Hot-swap subject matter expert plugins instantly — legal, medical, financial, technical. No reloads, no friction.",
};

export default function RootLayout({
    children,
}: Readonly<{ children: React.ReactNode }>) {
    return (
        <html lang="en" className={inter.variable}>
            <body className="font-sans antialiased">
                <PluginProvider>{children}</PluginProvider>
            </body>
        </html>
    );
}
