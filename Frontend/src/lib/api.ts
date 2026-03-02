// API Service for Backend Integration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://hackx-ybgm.onrender.com';

export interface ChatResponse {
  answer: string;
  confidence: number;
  sources: string[];
  methodology: string;
  domain: string;
  citations: string[];
  reasoning_steps: string[];
  disclaimer: string;
  multimodal_analysis?: {
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

export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
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
  multimodal_analysis?: any;
}

class ApiService {
  private baseUrl: string;
  private sessionId: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    // Generate or retrieve session ID (server-side simulation)
    this.sessionId = this.getOrCreateSessionId();
  }

  private getOrCreateSessionId(): string {
    // For server-side rendering, use a simple session ID generation
    // In a real app, this would come from server session management
    if (typeof window !== 'undefined') {
      let sessionId = sessionStorage.getItem('plugmind_session_id');
      
      if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('plugmind_session_id', sessionId);
      }
      
      return sessionId;
    }
    
    // Fallback for server-side rendering
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Send a multi-modal message with files to backend SME plugin with context
   */
  async sendMultiModalMessage(
    message: string, 
    files: Array<{
      id: string;
      name: string;
      type: string;
      data: string;
      preview?: string;
    }>,
    includeContext: boolean = true
  ): Promise<ChatResponse> {
    try {
      let contextPrompt = '';
      
      if (includeContext) {
        // Get context from backend
        contextPrompt = await this.getContextFromBackend();
      }

      // Prepare file data for backend
      const fileData = files.map(file => ({
        type: file.type,
        data: file.data,
        name: file.name
      }));

      const response = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          session_id: this.sessionId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Save message to backend
      await this.saveMessageToBackend(message, 'user', { files });
      await this.saveMessageToBackend(data.response, 'ai', {
        domain: data.domain,
        confidence: data.confidence,
        sources: data.sources,
        methodology: data.methodology,
        citations: data.citations,
        disclaimer: data.disclaimer,
        multimodal_analysis: data.multimodal_analysis
      });
      
      return data;
    } catch (error) {
      console.error('Error sending multi-modal message to backend:', error);
      throw error;
    }
  }

  /**
   * Send a message to backend SME plugin with context
   */
  async sendMessage(message: string, includeContext: boolean = true): Promise<ChatResponse> {
    try {
      let contextPrompt = '';
      
      if (includeContext) {
        // Get context from backend
        contextPrompt = await this.getContextFromBackend();
      }

      const response = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          user_id: 'frontend_user',
          session_id: this.sessionId,
          context: contextPrompt
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Save message to backend
      await this.saveMessageToBackend(message, 'user');
      await this.saveMessageToBackend(data.answer, 'ai', {
        domain: data.domain,
        confidence: data.confidence,
        sources: data.sources,
        methodology: data.methodology,
        citations: data.citations,
        disclaimer: data.disclaimer
      });
      
      return data;
    } catch (error) {
      console.error('Error sending message to backend:', error);
      throw error;
    }
  }

  /**
   * Get context from backend
   */
  private async getContextFromBackend(): Promise<string> {
    try {
      const response = await fetch(`${this.baseUrl}/context/${this.sessionId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        return data.context || '';
      }
    } catch (error) {
      console.error('Error getting context:', error);
    }
    
    return '';
  }

  /**
   * Save message to backend MongoDB
   */
  private async saveMessageToBackend(
    message: string, 
    sender: 'user' | 'ai', 
    metadata?: any
  ): Promise<void> {
    try {
      await fetch(`${this.baseUrl}/save_message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: this.sessionId,
          user_id: 'frontend_user',
          message: message,
          sender: sender,
          ...metadata
        }),
      });
    } catch (error) {
      console.error('Error saving message:', error);
    }
  }

  /**
   * Get plugin information
   */
  async getPluginInfo(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/plugin/info`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting plugin info:', error);
      throw error;
    }
  }

  /**
   * Switch to a different domain
   */
  async switchDomain(domain: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/plugin/switch_domain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ domain }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.success || true;
    } catch (error) {
      console.error('Error switching domain:', error);
      return false;
    }
  }

  /**
   * Get chat history from backend
   */
  async getChatHistory(limit: number = 50): Promise<ChatMessage[]> {
    try {
      const response = await fetch(`${this.baseUrl}/history/${this.sessionId}?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        return data.messages || [];
      }
      return [];
    } catch (error) {
      console.error('Error getting chat history:', error);
      return [];
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Clear chat history
   */
  async clearChatHistory(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/clear_history/${this.sessionId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Generate new session ID
        this.sessionId = this.getOrCreateSessionId();
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error clearing chat history:', error);
      return false;
    }
  }
}

export const apiService = new ApiService();
export default apiService;
