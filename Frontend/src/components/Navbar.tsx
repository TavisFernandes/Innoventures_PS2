"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { usePlugin } from "@/context/PluginContext";
import { Menu, X } from "lucide-react";

const NAV_LINKS = ["Chat", "Plugins", "Docs", "Pricing", "Enterprise"];

export default function Navbar() {
    const { activePlugin } = usePlugin();
    const [scrolled, setScrolled] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 40);
        window.addEventListener("scroll", handleScroll, { passive: true });
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <motion.nav
            initial={{ opacity: 0 }}
            animate={{ opacity: scrolled ? 1 : 0.4 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className="fixed top-0 left-0 right-0 z-50 glass"
            style={{
                borderBottom: scrolled
                    ? "1px solid rgba(255,255,255,0.05)"
                    : "1px solid transparent",
            }}
        >
            <div className="w-full px-4 md:px-6 h-14 flex items-center justify-between">
                {/* Logo */}
                <a href="#" className="flex items-center gap-2 group">
                    <div
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-white font-bold text-xs"
                        style={{ background: activePlugin.accent }}
                    >
                        P
                    </div>
                    <span className="text-white/90 font-semibold text-[15px] tracking-tight">
                        PlugMind
                    </span>
                </a>

                {/* Center Links — Desktop */}
                <div className="hidden md:flex items-center gap-8">
                    {NAV_LINKS.map((link) => (
                        <a
                            key={link}
                            href={`#${link.toLowerCase()}`}
                            className="text-white/50 hover:text-white/90 text-[13px] font-medium tracking-tight transition-colors duration-200"
                        >
                            {link}
                        </a>
                    ))}
                </div>

                {/* Right CTA */}
                <div className="hidden md:flex items-center gap-3">
                    <a
                        href="/signin"
                        className="text-white/50 hover:text-white/90 text-[13px] font-medium transition-colors duration-200"
                    >
                        Sign In
                    </a>
                    <a href="/signup" className="btn-gradient text-[13px] py-2 px-5">
                        Get Started Free
                    </a>
                </div>

                {/* Mobile Toggle */}
                <button
                    className="md:hidden text-white/60"
                    onClick={() => setMobileOpen(!mobileOpen)}
                >
                    {mobileOpen ? <X size={20} /> : <Menu size={20} />}
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.25 }}
                        className="md:hidden glass overflow-hidden border-t border-white/5"
                    >
                        <div className="px-6 py-4 flex flex-col gap-3">
                            {NAV_LINKS.map((link) => (
                                <a
                                    key={link}
                                    href={`#${link.toLowerCase()}`}
                                    className="text-white/60 hover:text-white text-sm font-medium"
                                    onClick={() => setMobileOpen(false)}
                                >
                                    {link}
                                </a>
                            ))}
                            <button className="btn-gradient text-sm mt-2 w-full">
                                Get Started Free
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.nav>
    );
}
