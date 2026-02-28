import {
    Scale,
    Stethoscope,
    TrendingUp,
    Cpu,
    Users,
    Shield,
    Bot,
    type LucideIcon,
} from "lucide-react";

export interface Plugin {
    id: string;
    name: string;
    persona: string;
    description: string;
    accent: string;
    accentRgb: string;
    accentDim: string;
    icon: LucideIcon;
    systemPrompt: string;
    suggestedPrompts: string[];
}

export const PLUGINS: Plugin[] = [
    {
        id: "default",
        name: "General",
        persona: "AI Assistant",
        description: "A versatile AI assistant for general queries",
        accent: "#0050FF",
        accentRgb: "0, 80, 255",
        accentDim: "#003399",
        icon: Bot,
        systemPrompt:
            "You are a helpful, intelligent AI assistant. Respond clearly, concisely, and professionally.",
        suggestedPrompts: [
            "Summarize this document for me",
            "Help me draft an email",
            "Explain this concept simply",
            "Generate a project timeline",
        ],
    },
    {
        id: "legal",
        name: "Legal",
        persona: "Legal Expert",
        description: "Contract analysis, compliance, and legal research",
        accent: "#D4A017",
        accentRgb: "212, 160, 23",
        accentDim: "#A67C12",
        icon: Scale,
        systemPrompt:
            "You are a Legal Expert AI. Provide detailed legal analysis, contract review insights, and compliance guidance. Always note that your responses do not constitute legal advice.",
        suggestedPrompts: [
            "Review this NDA for red flags",
            "Explain GDPR compliance requirements",
            "Draft a cease and desist template",
            "What are the risks in this clause?",
        ],
    },
    {
        id: "medical",
        name: "Medical",
        persona: "Medical Advisor",
        description: "Clinical guidance, drug interactions, and health research",
        accent: "#00C9A7",
        accentRgb: "0, 201, 167",
        accentDim: "#009B82",
        icon: Stethoscope,
        systemPrompt:
            "You are a Medical Advisor AI. Provide evidence-based health information, drug interaction data, and clinical guidance. Always remind users to consult healthcare professionals.",
        suggestedPrompts: [
            "Check drug interactions for these medications",
            "Explain this lab result",
            "Summarize latest research on treatment X",
            "What are the differential diagnoses for…",
        ],
    },
    {
        id: "finance",
        name: "Finance",
        persona: "Financial Strategist",
        description: "Market analysis, portfolio strategy, and financial planning",
        accent: "#00FF88",
        accentRgb: "0, 255, 136",
        accentDim: "#00CC6D",
        icon: TrendingUp,
        systemPrompt:
            "You are a Financial Strategist AI. Provide market analysis, portfolio recommendations, and financial planning guidance. Note that responses are informational and not investment advice.",
        suggestedPrompts: [
            "Analyze this stock's fundamentals",
            "Create a diversified portfolio strategy",
            "Explain the impact of rate changes",
            "Compare ETF vs mutual fund options",
        ],
    },
    {
        id: "engineering",
        name: "Engineering",
        persona: "Engineering Lead",
        description: "System architecture, code review, and technical guidance",
        accent: "#00D6FF",
        accentRgb: "0, 214, 255",
        accentDim: "#00A8CC",
        icon: Cpu,
        systemPrompt:
            "You are an Engineering Lead AI. Provide system architecture guidance, code review insights, debugging help, and technical best practices.",
        suggestedPrompts: [
            "Review this system architecture",
            "Optimize this database query",
            "Suggest a CI/CD pipeline setup",
            "Debug this error trace",
        ],
    },
    {
        id: "hr",
        name: "HR",
        persona: "HR Specialist",
        description: "Talent management, policy development, and workforce analytics",
        accent: "#A855F7",
        accentRgb: "168, 85, 247",
        accentDim: "#8B3FD4",
        icon: Users,
        systemPrompt:
            "You are an HR Specialist AI. Provide guidance on talent acquisition, employee engagement, policy development, and workforce analytics.",
        suggestedPrompts: [
            "Draft an employee onboarding checklist",
            "Create a performance review template",
            "Suggest team engagement activities",
            "Analyze this attrition data",
        ],
    },
    {
        id: "cybersecurity",
        name: "Security",
        persona: "Security Analyst",
        description: "Threat analysis, vulnerability assessment, and security posture",
        accent: "#FF4444",
        accentRgb: "255, 68, 68",
        accentDim: "#CC3333",
        icon: Shield,
        systemPrompt:
            "You are a Cybersecurity Analyst AI. Provide threat intelligence, vulnerability assessments, security architecture reviews, and incident response guidance.",
        suggestedPrompts: [
            "Assess vulnerabilities in this setup",
            "Create an incident response plan",
            "Review this security architecture",
            "Explain this CVE and its impact",
        ],
    },
];

export function getPluginById(id: string): Plugin {
    return PLUGINS.find((p) => p.id === id) || PLUGINS[0];
}
