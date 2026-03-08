"use client";

import { useEffect, useRef, useCallback } from "react";
import { useScroll, useTransform, motion } from "framer-motion";

const FRAME_COUNT = 240;

function currentFrame(index: number) {
    // e.g., ezgif-frame-001.jpg
    return `/brain/ezgif-frame-${String(index).padStart(3, "0")}.jpg`;
}

export default function BrainSequence() {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const imagesRef = useRef<HTMLImageElement[]>([]);

    // Track complete page scroll
    const { scrollYProgress } = useScroll();

    // Map scroll 0-1 to frame 1-240
    const frameIndex = useTransform(scrollYProgress, [0, 1], [1, FRAME_COUNT]);

    const renderFrame = useCallback((index: number, canvas: HTMLCanvasElement, images: HTMLImageElement[]) => {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const img = images[index];
        if (img && img.complete) {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Calculate aspect ratio fit (cover)
            const canvasAspect = canvas.width / canvas.height;
            const imgAspect = img.width / img.height;
            let drawWidth, drawHeight, offsetX, offsetY;

            if (canvasAspect > imgAspect) {
                // Canvas is wider than image
                drawHeight = canvas.height;
                drawWidth = drawHeight * imgAspect;
                offsetX = (canvas.width - drawWidth) / 2;
                offsetY = 0;
            } else {
                // Image is wider than canvas
                drawWidth = canvas.width;
                drawHeight = drawWidth / imgAspect;
                offsetX = 0;
                offsetY = (canvas.height - drawHeight) / 2;
            }

            ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
        }
    }, []);

    useEffect(() => {
        // Preload images
        let loadedCount = 0;
        let isCancelled = false;

        for (let i = 1; i <= FRAME_COUNT; i++) {
            const img = new Image();
            img.src = currentFrame(i);

            img.onload = () => {
                if (isCancelled) return;
                loadedCount++;
                imagesRef.current[i] = img;

                // Draw first frame exactly once when it loads
                if (i === 1) {
                    renderFrame(1, canvasRef.current!, imagesRef.current);
                }
            };
        }

        return () => {
            isCancelled = true;
        };
    }, []);

    useEffect(() => {
        let animationFrameId: number;

        // Update canvas whenever scroll changes frame index
        const unsubscribe = frameIndex.on("change", (latest) => {
            const roundedIndex = Math.min(FRAME_COUNT, Math.max(1, Math.round(latest)));
            if (animationFrameId) cancelAnimationFrame(animationFrameId);
            animationFrameId = requestAnimationFrame(() => renderFrame(roundedIndex, canvasRef.current!, imagesRef.current));
        });

        // Handle resize
        const handleResize = () => {
            if (canvasRef.current) {
                // Use a smaller internal resolution to ensure performance and reliable draws
                const dpr = typeof window !== 'undefined' ? window.devicePixelRatio || 1 : 1;
                canvasRef.current.width = window.innerWidth * dpr;
                canvasRef.current.height = window.innerHeight * dpr;
                renderFrame(Math.min(FRAME_COUNT, Math.max(1, Math.round(frameIndex.get()))), canvasRef.current!, imagesRef.current);
            }
        };

        // Initial size
        handleResize();

        window.addEventListener("resize", handleResize);
        return () => {
            unsubscribe();
            window.removeEventListener("resize", handleResize);
            if (animationFrameId) cancelAnimationFrame(animationFrameId);
        };
    }, [frameIndex]);

    // Use opacity and scale transforms based on scroll to make it fade out smoothly towards the end
    const opacity = useTransform(scrollYProgress, [0, 0.8, 1], [1, 0.4, 0]);
    const scale = useTransform(scrollYProgress, [0, 1], [1, 1.2]);

    return (
        <motion.div
            className="fixed inset-0 w-full h-full pointer-events-none -z-10"
            style={{ opacity, scale }}
        >
            <canvas
                ref={canvasRef}
                className="w-full h-full object-cover"
                style={{
                    filter: "contrast(1.2) brightness(1.1)",
                }}
            />
            {/* Dark overlay without multiply to ensure text stays readable */}
            <div className="absolute inset-0 bg-brand-bg/40 pointer-events-none" />
        </motion.div>
    );
}
