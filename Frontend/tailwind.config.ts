import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    bg: "#050505",
                    surface: "#0A0A0C",
                    card: "#111114",
                    border: "#1a1a1f",
                },
                plugin: {
                    default: "#0050FF",
                    legal: "#D4A017",
                    medical: "#00C9A7",
                    finance: "#00FF88",
                    engineering: "#00D6FF",
                    hr: "#A855F7",
                },
            },
            fontFamily: {
                sans: ["Inter", "SF Pro Display", "system-ui", "sans-serif"],
            },
            animation: {
                "glow-pulse": "glow-pulse 2s ease-in-out infinite",
                "fade-in": "fade-in 0.6s ease-out",
                "slide-up": "slide-up 0.5s ease-out",
                "slide-left": "slide-left 0.5s ease-out",
                "slide-right": "slide-right 0.5s ease-out",
            },
            keyframes: {
                "glow-pulse": {
                    "0%, 100%": { opacity: "0.4" },
                    "50%": { opacity: "0.8" },
                },
                "fade-in": {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
                "slide-up": {
                    "0%": { opacity: "0", transform: "translateY(20px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
                "slide-left": {
                    "0%": { opacity: "0", transform: "translateX(40px)" },
                    "100%": { opacity: "1", transform: "translateX(0)" },
                },
                "slide-right": {
                    "0%": { opacity: "0", transform: "translateX(-40px)" },
                    "100%": { opacity: "1", transform: "translateX(0)" },
                },
            },
        },
    },
    plugins: [],
};
export default config;
