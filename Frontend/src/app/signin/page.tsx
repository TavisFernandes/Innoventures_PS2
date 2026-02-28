"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeft, Mail, Lock, Eye, EyeOff } from "lucide-react";
import Link from "next/link";

export default function SignIn() {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        rememberMe: false,
    });

    const [errors, setErrors] = useState<Record<string, string>>({});
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const validateForm = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.email.trim()) {
            newErrors.email = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            newErrors.email = "Please enter a valid email";
        }

        if (!formData.password) {
            newErrors.password = "Password is required";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type, checked } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value,
        }));
        // Clear error for this field when user starts typing
        if (errors[name]) {
            setErrors((prev) => ({
                ...prev,
                [name]: "",
            }));
        }
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        setLoading(true);

        // Simulate API call
        try {
            await new Promise((resolve) => setTimeout(resolve, 2000));
            setSuccess(true);
            setFormData({
                email: "",
                password: "",
                rememberMe: false,
            });

            // Redirect after success
            setTimeout(() => {
                window.location.href = "/";
            }, 2000);
        } catch (error) {
            setErrors({ submit: "Something went wrong. Please try again." });
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen relative bg-gradient-to-b from-[#050505] via-[#0a0a0a] to-[#050505] flex items-center justify-center px-4 py-12">
            {/* Ambient background */}
            <div className="fixed inset-0 pointer-events-none">
                <div className="absolute top-0 right-1/4 w-96 h-96 bg-blue-600/5 rounded-full blur-3xl"></div>
                <div className="absolute bottom-1/4 left-1/3 w-96 h-96 bg-blue-500/3 rounded-full blur-3xl"></div>
            </div>

            <div className="w-full max-w-md relative z-10">
                {/* Back button */}
                <Link
                    href="/"
                    className="inline-flex items-center gap-2 text-white/50 hover:text-white/90 text-sm font-medium transition-colors mb-8 group"
                >
                    <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
                    Back to home
                </Link>

                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="mb-8"
                >
                    <h1 className="text-3xl font-bold text-white mb-2">Welcome back</h1>
                    <p className="text-white/60 text-sm">
                        Sign in to access your PlugMind dashboard
                    </p>
                </motion.div>

                {/* Form Card */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="glass gradient-border p-6 rounded-2xl"
                >
                    {success && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="mb-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg text-green-400 text-sm"
                        >
                            ✓ Signed in successfully! Redirecting...
                        </motion.div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {/* Email Field */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    placeholder="you@example.com"
                                    className="w-full pl-10 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-white placeholder-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/8 transition-all"
                                />
                            </div>
                            {errors.email && <p className="text-red-400/90 text-xs mt-1.5">{errors.email}</p>}
                        </div>

                        {/* Password Field */}
                        <div>
                            <label className="block text-white/90 text-sm font-medium mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
                                <input
                                    type={showPassword ? "text" : "password"}
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder="••••••••"
                                    className="w-full pl-10 pr-11 py-2.5 bg-white/5 border border-white/10 rounded-lg text-white placeholder-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/8 transition-all"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors"
                                >
                                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                                </button>
                            </div>
                            {errors.password && (
                                <p className="text-red-400/90 text-xs mt-1.5">{errors.password}</p>
                            )}
                        </div>

                        {/* Remember Me & Forgot Password */}
                        <div className="flex items-center justify-between">
                            <label className="flex items-center gap-2 cursor-pointer group">
                                <input
                                    type="checkbox"
                                    name="rememberMe"
                                    checked={formData.rememberMe}
                                    onChange={handleChange}
                                    className="w-4 h-4 rounded bg-white/5 border border-white/10 text-blue-500 cursor-pointer"
                                />
                                <span className="text-white/60 text-sm group-hover:text-white/80 transition-colors">
                                    Remember me
                                </span>
                            </label>
                            <a
                                href="#"
                                className="text-blue-400 hover:text-blue-300 text-sm font-medium transition-colors"
                            >
                                Forgot password?
                            </a>
                        </div>

                        {errors.submit && (
                            <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm">
                                {errors.submit}
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full btn-gradient py-3 mt-6 disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                            {loading ? "Signing in..." : "Sign In"}
                        </button>

                        {/* Divider */}
                        <div className="flex items-center gap-3 my-5">
                            <div className="flex-1 h-px bg-white/10"></div>
                            <span className="text-white/40 text-xs">or</span>
                            <div className="flex-1 h-px bg-white/10"></div>
                        </div>

                        {/* Social Login (placeholder) */}
                        <div className="grid grid-cols-2 gap-3">
                            <button type="button" className="btn-outline py-2.5">
                                Google
                            </button>
                            <button type="button" className="btn-outline py-2.5">
                                GitHub
                            </button>
                        </div>

                        {/* Sign Up Link */}
                        <p className="text-center text-white/60 text-sm mt-6">
                            Don't have an account?{" "}
                            <Link
                                href="/signup"
                                className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                            >
                                Sign up
                            </Link>
                        </p>
                    </form>
                </motion.div>

                {/* Footer text */}
                <p className="text-center text-white/40 text-xs mt-6">
                    Need help?{" "}
                    <a href="#" className="text-blue-400 hover:text-blue-300 transition-colors">
                        Contact support
                    </a>
                </p>
            </div>
        </main>
    );
}
