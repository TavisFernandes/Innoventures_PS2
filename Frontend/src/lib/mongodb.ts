// MongoDB Service for Chat History Management (Disabled for Vercel Deployment)
// import { MongoClient, Db, Collection } from 'mongodb';

interface ChatMessage {
  _id?: string;
  sessionId: string;
  userId: string;
  message: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  domain?: string;
  confidence?: number;
  sources?: string[];
  methodology?: string;
  citations?: string[];
  disclaimer?: string;
}

interface ChatSession {
  _id?: string;
  sessionId: string;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  messageCount: number;
  lastMessage?: string;
  domain?: string;
}

class MongoDBService {
  // Disabled for Vercel deployment - use local storage or API instead
  private readonly MONGODB_URI = process.env.NEXT_PUBLIC_MONGODB_URI || 'mongodb://localhost:27017/';
  
  async connect(): Promise<void> {
    console.log('MongoDB service disabled for Vercel deployment');
  }

  async disconnect(): Promise<void> {
    console.log('MongoDB service disabled for Vercel deployment');
  }

  async createOrUpdateSession(sessionId: string, userId: string = 'default_user'): Promise<void> {
    // No-op for Vercel deployment
  }

  async saveMessage(
    sessionId: string,
    userId: string,
    message: string,
    sender: 'user' | 'ai',
    metadata?: {
      domain?: string;
      confidence?: number;
      sources?: string[];
      methodology?: string;
      citations?: string[];
      disclaimer?: string;
    }
  ): Promise<void> {
    // No-op for Vercel deployment
  }

  async getChatHistory(
    sessionId: string, 
    userId: string = 'default_user',
    limit: number = 50
  ): Promise<ChatMessage[]> {
    // Return empty history for Vercel deployment
    return [];
  }

  async getContextMessages(
    sessionId: string,
    userId: string = 'default_user',
    contextLimit: number = 10
  ): Promise<ChatMessage[]> {
    // Return empty context for Vercel deployment
    return [];
  }

  async searchMessages(
    sessionId: string,
    userId: string = 'default_user',
    query: string,
    limit: number = 20
  ): Promise<ChatMessage[]> {
    // Return empty results for Vercel deployment
    return [];
  }

  async getSessionInfo(sessionId: string): Promise<ChatSession | null> {
    // Return null for Vercel deployment
    return null;
  }

  async deleteSession(sessionId: string, userId: string = 'default_user'): Promise<void> {
    // No-op for Vercel deployment
  }

  async getAllSessions(userId: string = 'default_user'): Promise<ChatSession[]> {
    // Return empty list for Vercel deployment
    return [];
  }

  async generateContextPrompt(
    sessionId: string,
    userId: string = 'default_user',
    maxContextMessages: number = 8
  ): Promise<string> {
    // Return empty context for Vercel deployment
    return '';
  }
}

// Export singleton instance
const mongoDBService = new MongoDBService();

export type { ChatMessage, ChatSession };
export { mongoDBService };
export default mongoDBService;
