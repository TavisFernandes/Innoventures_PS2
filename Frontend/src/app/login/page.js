'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const { user: authUser } = useAuth();
  const router = useRouter();

  // Redirect if already logged in
  if (authUser) {
    router.push('/');
    return null;
  }

  const [loading, setLoading] = useState(false);

  // Auto-redirect to main page without requiring login
  useEffect(() => {
    // Simulate immediate login for demo
    router.push('/');
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">PlugMind AI</h1>
          <p className="text-gray-600">Your AI-powered financial assistant</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-xl shadow-xl p-8 space-y-6">
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full mx-auto mb-4 flex items-center justify-center">
              <span className="text-white text-2xl font-bold">PM</span>
            </div>
            <h2 className="text-xl font-semibold text-gray-900">Welcome Back</h2>
            <p className="text-gray-600 text-sm">Redirecting to main app...</p>
          </div>

          {/* Features */}
          <div className="mt-6 text-center">
            <div className="text-sm text-gray-600 space-y-2">
              <p className="flex items-center justify-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                AI-powered responses
              </p>
              <p className="flex items-center justify-center gap-2">
                <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                Chat history saved
              </p>
              <p className="flex items-center justify-center gap-2">
                <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                Multiple expert domains
              </p>
            </div>
          </div>

          {/* Redirect Message */}
          <div className="text-center">
            <p className="text-sm text-blue-600">
              You will be redirected automatically...
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
