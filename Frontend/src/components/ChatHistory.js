'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { motion } from 'framer-motion';
import { FiMessageSquare, FiClock, FiTrash2, FiArrowRight } from 'react-icons/fi';

export default function ChatHistory() {
  const { user } = useAuth();
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchUserChatHistory = async () => {
      try {
        const response = await fetch(`https://hackx-2.onrender.com/user-history/${user.uid}`);
        const data = await response.json();
        
        if (data.sessions) {
          const formattedChats = data.sessions.map(session => ({
            id: session.session_id,
            lastUpdated: session.updated_at,
            messageCount: session.message_count || 0,
            lastMessage: session.last_message || 'No messages yet',
            createdAt: session.created_at
          }));
          setChatHistory(formattedChats);
        }
      } catch (error) {
        console.error('Error fetching chat history:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserChatHistory();
  }, [user]);

  const deleteChat = async (chatId) => {
    if (!user) return;
    
    try {
      await fetch(`https://hackx-2.onrender.com/clear_history/${chatId}`, {
        method: 'DELETE'
      });
      setChatHistory(prev => prev.filter(chat => chat.id !== chatId));
    } catch (error) {
      console.error('Error deleting chat:', error);
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleContinueChat = (chatId) => {
    localStorage.setItem('currentSessionId', chatId);
    window.location.href = '/chat';
  };

  if (!user) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 bg-gradient-to-br from-indigo-500 to-purple-600">
            <FiMessageSquare className="w-8 h-8 text-white" />
          </div>
          <p className="text-white/80 text-lg">Please sign in to view your chat history</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6">
      {loading ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center h-full"
        >
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4 bg-gradient-to-br from-indigo-500 to-purple-600">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-white/30 border-t-white"></div>
          </div>
          <p className="text-white/80 text-lg">Loading your conversations...</p>
        </motion.div>
      ) : chatHistory.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center h-full text-center"
        >
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 bg-gradient-to-br from-indigo-500 to-purple-600">
            <FiMessageSquare className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-xl font-semibold text-white mb-2">No conversations yet</h3>
          <p className="text-white/60">Start your first chat to see it here</p>
        </motion.div>
      ) : (
        <div className="space-y-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <h2 className="text-2xl font-bold text-white mb-2">Your Conversations</h2>
            <p className="text-white/80">Continue your previous discussions or start new ones</p>
          </motion.div>

          <div className="space-y-3">
            {chatHistory.map((chat, index) => (
              <motion.div
                key={chat.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="group relative"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-600/20 rounded-[1.5rem] blur-xl group-hover:from-indigo-500/30 group-hover:to-purple-600/30 transition-all duration-300"></div>
                
                <div className="relative bg-black/40 backdrop-blur-xl border border-white/10 rounded-[1.5rem] p-6 hover:border-white/20 transition-all duration-300 cursor-pointer group">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                          <FiMessageSquare className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="text-white font-semibold truncate">
                            {chat.lastMessage?.substring(0, 60) || 'New Conversation'}
                          </h3>
                          <div className="flex items-center gap-2 text-sm text-white/60">
                            <FiClock className="w-4 h-4" />
                            <span>{formatDate(chat.lastUpdated)}</span>
                            <span className="text-white/40">•</span>
                            <span>{chat.messageCount || 0} messages</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2 ml-4">
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleContinueChat(chat.id);
                        }}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl text-sm font-medium hover:from-indigo-600 hover:to-purple-700 transition-all duration-300"
                      >
                        Continue
                        <FiArrowRight className="w-4 h-4" />
                      </motion.button>
                      
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteChat(chat.id);
                        }}
                        className="p-2 text-white/60 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition-all duration-300"
                      >
                        <FiTrash2 className="w-4 h-4" />
                      </motion.button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
