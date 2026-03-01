// File Upload Service for Multi-Modal Chat
export interface FileUpload {
  id: string;
  name: string;
  type: string;
  size: number;
  data: string;
  preview?: string;
}

export interface MultiModalMessage {
  text: string;
  files: FileUpload[];
  timestamp: Date;
}

class FileUploadService {
  private static readonly MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  private static readonly ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain'];
  private static readonly MAX_FILES = 5;

  static validateFile(file: File): { valid: boolean; error?: string } {
    // Check file size
    if (file.size > this.MAX_FILE_SIZE) {
      return { valid: false, error: `File size exceeds ${this.MAX_FILE_SIZE / (1024 * 1024)}MB limit` };
    }

    // Check file type
    if (!this.ALLOWED_TYPES.includes(file.type)) {
      return { valid: false, error: `File type ${file.type} not allowed` };
    }

    return { valid: true };
  }

  static async processFile(file: File): Promise<FileUpload> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const result = e.target?.result;
        if (typeof result === 'string') {
          resolve({
            id: `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            name: file.name,
            type: file.type,
            size: file.size,
            data: result,
            preview: this.generatePreview(file.type, result)
          });
        } else {
          reject(new Error('Failed to process file'));
        }
      };

      reader.onerror = () => reject(new Error('Failed to read file'));
      
      if (file.type.startsWith('image/')) {
        reader.readAsDataURL(file);
      } else if (file.type === 'application/pdf') {
        reader.readAsText(file);
      } else {
        reader.readAsText(file);
      }
    });
  }

  static generatePreview(fileType: string, data: string): string {
    if (fileType.startsWith('image/')) {
      return data; // Data URL for images
    } else if (fileType === 'application/pdf') {
      return `PDF Document (${data.length} characters)`;
    } else {
      return data.substring(0, 100) + (data.length > 100 ? '...' : '');
    }
  }

  static formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    const f = Math.min(bytes / Math.pow(k, i), 3);
    return parseFloat((f).toFixed(2)) + ' ' + sizes[i];
  }
}

export default FileUploadService;
