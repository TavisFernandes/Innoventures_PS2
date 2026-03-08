'use client';

import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import Navbar from '@/components/Navbar';
import ChatPanel from '@/components/ChatPanel';
import ChatHistory from '@/components/ChatHistory';
import { FiMessageSquare, FiLogOut, FiClock } from 'react-icons/fi';

export default function ChatPage() {
  const { user, signOut } = useAuth();
  const [showHistory, setShowHistory] = useState(false);

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">PlugMind AI</h1>
          <p className="text-gray-600 mb-6">Please sign in to access your AI assistant</p>
          <a 
            href="/login" 
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Sign In with Google
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
        
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 min-h-screen">
          <div className="p-4">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">
                {showHistory ? 'Chat History' : 'AI Assistant'}
              </h2>
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
              >
                {showHistory ? <FiMessageSquare className="w-5 h-5" /> : <FiClock className="w-5 h-5" />}
              </button>
            </div>
              
            {/* User Info */}
            <div className="flex items-center space-x-3 mb-6 p-3 bg-gray-50 rounded-lg">
              <img 
                src={user.photoURL || '/default-avatar.png'} 
                alt={user.displayName || 'User'} 
                className="w-10 h-10 rounded-full"
              />
              <div>
                <p className="text-sm font-medium text-gray-900">{user.displayName || 'User'}</p>
                <p className="text-xs text-gray-500">{user.email}</p>
              </div>
            </div>

            {/* Sign Out Button */}
            <button
              onClick={signOut}
              className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm text-red-600 hover:text-red-700 rounded-lg hover:bg-red-50"
            >
              <FiLogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>

          {/* Navigation */}
          <div className="px-4 pb-4">
            <div className="space-y-2">
              <button
                onClick={() => setShowHistory(false)}
                className={`w-full text-left px-3 py-2 text-sm rounded-lg ${
                  !showHistory 
                    ? 'bg-indigo-100 text-indigo-700' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <FiMessageSquare className="w-4 h-4 inline mr-3" />
                New Chat
              </button>
              <button
                onClick={() => setShowHistory(true)}
                className={`w-full text-left px-3 py-2 text-sm rounded-lg ${
                  showHistory 
                    ? 'text-gray-700 hover:bg-gray-100' 
                    : 'bg-indigo-100 text-indigo-700'
                }`}
              >
                <FiClock className="w-4 h-4 inline mr-3" />
                Chat History
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="w-full text-left px-3 py-2 text-sm rounded-lg text-gray-700 hover:bg-gray-100"
              >
                ← Back to Home
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {showHistory ? <ChatHistory /> : <ChatPanel />}
        </div>
      </div>
    </div>
  );
}
