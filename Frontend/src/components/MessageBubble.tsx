"use client";

import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import { Check, CheckCheck, Copy, Download, Sparkles } from "lucide-react";
import { usePlugin } from "@/context/PluginContext";

import { Bot, User, BookOpen, TrendingUp, Scale, Briefcase, ExternalLink, CheckCircle, AlertCircle, FileText } from "lucide-react";

import { useState } from "react";



interface MessageBubbleProps {

    message: string;

    sender: "user" | "ai";

    index: number;

    domain?: string;

    confidence?: number;

    sources?: string[];

    methodology?: string;

    citations?: string[];

    disclaimer?: string;

    files?: Array<{

        id: string;

        name: string;

        type: string;

        size: number;

        preview?: string;

    }>;

    multimodalAnalysis?: {

        text_analysis: string;

        file_analysis: Array<{

            type: string;

            content: string;

            extracted_entities?: string[];

            ocr_text?: string;

            sentiment?: any;

        }>;

        cross_reference: {};

        confidence: number;

    };

}



const getDomainIcon = (domain?: string) => {

    switch (domain) {

        case 'legal':

        case 'contract_law':

        case 'corporate_law':

            return Scale;

        case 'finance':

        case 'investment':

        case 'banking':

        case 'loan_analysis':

            return TrendingUp;

        case 'regulatory_compliance':

            return Briefcase;

        default:

            return BookOpen;

    }

};



const getDomainColor = (domain?: string, accent?: string) => {

    switch (domain) {

        case 'legal':

        case 'contract_law':

        case 'corporate_law':

            return '#ef4444'; // red

        case 'finance':

        case 'investment':

        case 'banking':

        case 'loan_analysis':

            return '#22c55e'; // green

        case 'regulatory_compliance':

            return '#3b82f6'; // blue

        default:

            return accent || '#8b5cf6'; // purple

    }

};



const formatMessage = (text: string) => {

    // Convert markdown-like formatting to HTML

    if (!text || typeof text !== 'string') {

        return '';

    }

    

    let formatted = text;

    

    // Bold text **text**

    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    

    // Italic text *text*

    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    

    // Headers ### Header

    formatted = formatted.replace(/^### (.*$)/gm, '<h3 class="text-lg font-semibold mt-4 mb-2 text-white/80">$1</h3>');

    

    // Headers ## Header

    formatted = formatted.replace(/^## (.*$)/gm, '<h2 class="text-xl font-semibold mt-4 mb-2 text-white/90">$1</h2>');

    

    // Headers # Header

    formatted = formatted.replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-4 mb-3 text-white">$1</h1>');

    

    // Bullet points - item or * item

    formatted = formatted.replace(/^[\-\*]\s+(.*$)/gm, '<li class="ml-4 mb-1 text-white/70">• $1</li>');

    

    // Numbered lists 1. item

    formatted = formatted.replace(/^\d+\.\s+(.*$)/gm, '<li class="ml-4 mb-1 text-white/70">$1</li>');

    

    // Line breaks

    formatted = formatted.replace(/\n\n/g, '<br /><br />');

    formatted = formatted.replace(/\n/g, '<br />');

    

    return formatted;

};



const extractCitations = (text: string) => {

    const citationRegex = /\[(\d+)\]/g;

    const citations = [];

    let match;

    

    while ((match = citationRegex.exec(text)) !== null) {

        citations.push({

            index: match[1],

            position: match.index,

            text: match[0]

        });

    }

    

    return citations;

};



const renderClickableCitations = (text: string, onCitationClick: (index: string) => void) => {

    if (!text || typeof text !== 'string') {

        return '';

    }

    

    const citations = extractCitations(text);

    let formattedText = text;

    

    // Replace citations with clickable elements

    citations.forEach(citation => {

        const citationElement = `<span class="citation-link cursor-pointer text-blue-400 hover:text-blue-300 underline" data-citation="${citation.index}">[${citation.index}]</span>`;

        formattedText = formattedText.replace(citation.text, citationElement);

    });

    

    return formattedText;

};



export default function MessageBubble({ 

    message, 

    sender, 

    index, 

    domain, 

    confidence, 

    sources, 

    methodology, 

    citations, 

    disclaimer,

    files,

    multimodalAnalysis 

}: MessageBubbleProps) {

    const { activePlugin } = usePlugin();

    const isAI = sender === "ai";

    const [showDetails, setShowDetails] = useState(false);

    const [expandedCitations, setExpandedCitations] = useState<Set<string>>(new Set());

    const [showFiles, setShowFiles] = useState(false);

    

    const DomainIcon = getDomainIcon(domain);

    const domainColor = getDomainColor(domain, activePlugin.accent);

    

    const handleCitationClick = (citationIndex: string) => {

        setExpandedCitations(prev => {

            const newSet = new Set(prev);

            if (newSet.has(citationIndex)) {

                newSet.delete(citationIndex);

            } else {

                newSet.add(citationIndex);

            }

            return newSet;

        });

    };

    

    const formattedMessage = formatMessage(message);

    const messageWithClickableCitations = renderClickableCitations(formattedMessage, handleCitationClick);



    return (

        <motion.div

            initial={{ opacity: 0, y: 12 }}

            animate={{ opacity: 1, y: 0 }}

            transition={{ duration: 0.35, delay: index * 0.08, ease: [0.25, 0.1, 0.25, 1] }}

            className={`flex gap-3 ${isAI ? "justify-start" : "justify-end"}`}

        >

            {isAI && (

                <div

                    className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-1"

                    style={{

                        background: `${domainColor}20`,

                        color: domainColor,

                    }}

                >

                    <DomainIcon size={16} />

                </div>

            )}



            <div className={`max-w-[80%] space-y-3`}>

                {/* File Display */}

                {files && files.length > 0 && (

                    <div className="bg-gray-50 rounded-lg p-3 mb-3 border border-gray-200">

                        <div className="flex items-center justify-between mb-2">

                            <span className="text-sm font-medium text-gray-700">

                                📎 Attached Files ({files.length})

                            </span>

                            <button

                                onClick={() => setShowFiles(!showFiles)}

                                className="text-blue-500 hover:text-blue-700 text-sm"

                            >

                                {showFiles ? 'Hide' : 'Show'}

                            </button>

                        </div>

                        

                        {showFiles && (

                            <div className="space-y-2">

                                {files.map((file, i) => (

                                    <div key={file.id} className="flex items-center space-x-3 p-2 bg-white rounded border border-gray-200">

                                        {file.type.startsWith('image/') ? (

                                            <div className="w-16 h-16 rounded overflow-hidden">

                                                <Image

                                                    src={file.preview || ''}

                                                    alt={file.name}

                                                    width={64}

                                                    height={64}

                                                    className="w-full h-full object-cover"

                                                />

                                            </div>

                                        ) : file.type === 'application/pdf' ? (

                                            <div className="flex items-center space-x-2">

                                                <FileText className="w-8 h-8 text-red-500" />

                                                <div className="text-sm">

                                                    <div className="font-medium">{file.name}</div>

                                                    <div className="text-gray-500">{file.preview}</div>

                                                </div>

                                            </div>

                                        ) : (

                                            <div className="flex items-center space-x-2">

                                                <FileText className="w-8 h-8 text-blue-500" />

                                                <div className="text-sm">

                                                    <div className="font-medium">{file.name}</div>

                                                    <div className="text-gray-500">{(file.size / 1024).toFixed(1)}KB</div>

                                                </div>

                                            </div>

                                        )}

                                    </div>

                                ))}

                            </div>

                        )}

                    </div>

                )}



                {/* Multi-Modal Analysis Display */}

                {multimodalAnalysis && (

                    <div className="bg-blue-50 rounded-lg p-3 mb-3 border border-blue-200">

                        <div className="flex items-center justify-between mb-2">

                            <span className="text-sm font-medium text-blue-700">

                                🔍 Multi-Modal Analysis

                            </span>

                            <span className="text-xs text-blue-500">

                                Confidence: {Math.round(multimodalAnalysis.confidence * 100)}%

                            </span>

                        </div>

                        

                        <div className="space-y-2">

                            {multimodalAnalysis.file_analysis.map((analysis, i) => (

                                <div key={i} className="text-xs text-gray-600">

                                    <div className="font-medium">{analysis.type.toUpperCase()}:</div>

                                    <div className="mt-1">{analysis.content}</div>

                                    {analysis.extracted_entities && analysis.extracted_entities.length > 0 && (

                                        <div className="mt-1">

                                            <div className="font-medium">Extracted Entities:</div>

                                            <div className="text-blue-600">{analysis.extracted_entities.join(', ')}</div>

                                        </div>

                                    )}

                                </div>

                            ))}

                        </div>

                    </div>

                )}



                {/* Main Message */}

                <div

                    className={`

                        rounded-2xl px-5 py-4 text-[14px] leading-relaxed

                        ${isAI

                            ? "bg-white/[0.04] text-white/70 border-l-[3px]"

                            : "bg-white/[0.08] text-white/80"

                        }

                    `}

                    style={

                        isAI

                            ? { borderLeftColor: domainColor }

                            : undefined

                    }

                >

                    <div 

                        dangerouslySetInnerHTML={{ __html: messageWithClickableCitations }}

                        className="prose prose-invert max-w-none"

                        onClick={(e) => {

                            const target = e.target as HTMLElement;

                            if (target.classList.contains('citation-link')) {

                                const citationIndex = target.getAttribute('data-citation');

                                if (citationIndex) {

                                    handleCitationClick(citationIndex);

                                }

                            }

                        }}

                    />

                    

                    {/* Domain and Confidence Badge */}

                    {isAI && domain && (

                        <div className="mt-4 pt-3 border-t border-white/[0.1] flex items-center justify-between">

                            <div className="flex items-center gap-2">

                                <DomainIcon size={12} style={{ color: domainColor }} />

                                <span className="text-[11px] font-medium text-white/50">

                                    {domain ? domain.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'Unknown'}

                                </span>

                            </div>

                            <div className="flex items-center gap-2">

                                {confidence && (

                                    <span className="text-[11px] text-white/40">

                                        {Math.round(confidence * 100)}% confidence

                                    </span>

                                )}

                                <CheckCircle size={12} className="text-green-400" />

                            </div>

                        </div>

                    )}

                </div>



                {/* Expandable Details */}

                {isAI && (sources || methodology || citations) && (

                    <div className="space-y-2">

                        <button

                            onClick={() => setShowDetails(!showDetails)}

                            className="flex items-center gap-2 text-[11px] text-white/40 hover:text-white/60 transition-colors"

                        >

                            <ExternalLink size={12} />

                            {showDetails ? 'Hide' : 'Show'} Sources & Details

                        </button>

                        

                        {showDetails && (

                            <motion.div

                                initial={{ opacity: 0, height: 0 }}

                                animate={{ opacity: 1, height: 'auto' }}

                                exit={{ opacity: 0, height: 0 }}

                                className="bg-white/[0.02] rounded-lg p-4 space-y-3 border border-white/[0.05]"

                            >

                                {methodology && (

                                    <div className="space-y-2">

                                        <div className="flex items-center gap-2 text-[12px] font-medium text-white/50">

                                            <AlertCircle size={12} />

                                            Methodology

                                        </div>

                                        <div className="text-[11px] text-white/40 leading-relaxed">

                                            {methodology}

                                        </div>

                                    </div>

                                )}

                                

                                {sources && sources.length > 0 && (

                                    <div className="space-y-2">

                                        <div className="flex items-center gap-2 text-[12px] font-medium text-white/50">

                                            <BookOpen size={12} />

                                            Sources

                                        </div>

                                        <ul className="space-y-1">

                                            {sources.slice(0, 5).map((source, i) => (

                                                <li key={i} className="text-[11px] text-white/30 flex items-start gap-2">

                                                    <span className="text-white/20 mt-1">•</span>

                                                    <span>{source}</span>

                                                </li>

                                            ))}

                                        </ul>

                                    </div>

                                )}

                                

                                {citations && citations.length > 0 && (

                                    <div className="space-y-2">

                                        <div className="flex items-center gap-2 text-[12px] font-medium text-white/50">

                                            <ExternalLink size={12} />

                                            Citations

                                        </div>

                                        <div className="space-y-1">

                                            {citations.map((citation, i) => (

                                                <div key={i} className="text-[11px] text-white/30">

                                                    <span 

                                                        className="cursor-pointer text-blue-400 hover:text-blue-300"

                                                        onClick={() => handleCitationClick(citation)}

                                                    >

                                                        [{citation}]

                                                    </span>

                                                    {expandedCitations.has(citation) && (

                                                        <div className="mt-1 p-2 bg-white/[0.05] rounded text-[10px] text-white/40">

                                                            Citation {citation} - This reference supports the claims made in the response above.

                                                        </div>

                                                    )}

                                                </div>

                                            ))}

                                        </div>

                                    </div>

                                )}

                                

                                {disclaimer && (

                                    <div className="pt-3 border-t border-white/[0.1]">

                                        <div className="text-[10px] text-white/30 italic">

                                            <AlertCircle size={10} className="inline mr-1" />

                                            {disclaimer}

                                        </div>

                                    </div>

                                )}

                            </motion.div>

                        )}

                    </div>

                )}

            </div>



            {!isAI && (

                <div className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center mt-1 bg-white/[0.06] text-white/40">

                    <User size={16} />

                </div>

            )}

        </motion.div>

    );

}

