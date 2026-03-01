"use client";

import { useState, useRef } from "react";
import { Plus, X, FileText, Image } from "lucide-react";
import FileUploadService, { FileUpload } from "@/lib/fileUpload";

interface FileUploadComponentProps {
  onFilesSelected: (files: FileUpload[]) => void;
  disabled?: boolean;
}

export default function FileUploadComponent({ onFilesSelected, disabled = false }: FileUploadComponentProps) {
  const [files, setFiles] = useState<FileUpload[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    processFiles(droppedFiles as File[]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    processFiles(selectedFiles as File[]);
  };

  const processFiles = async (newFiles: File[]) => {
    const validFiles = [];
    
    for (const file of newFiles) {
      const validation = FileUploadService.validateFile(file);
      if (validation.valid) {
        const processedFile = await FileUploadService.processFile(file);
        validFiles.push(processedFile);
      }
    }

    const updatedFiles = [...files, ...validFiles].slice(0, 3);
    setFiles(updatedFiles);
    onFilesSelected(updatedFiles);
  };

  const removeFile = (fileId: string) => {
    const updatedFiles = files.filter(f => f.id !== fileId);
    setFiles(updatedFiles);
    onFilesSelected(updatedFiles);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="flex items-center gap-2">
      {/* Compact Upload Button */}
      <button
        onClick={openFileDialog}
        disabled={disabled}
        className={`
          flex items-center gap-2 px-3 py-2 rounded-lg border-2 transition-all
          ${isDragging 
            ? 'border-blue-400 bg-blue-50 text-blue-600' 
            : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
          }
          ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <Plus size={16} />
        <span className="text-sm font-medium">Add Files</span>
      </button>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*,.pdf,text/plain"
        onChange={handleFileSelect}
        disabled={disabled}
        className="hidden"
      />

      {/* Compact File List */}
      {files.length > 0 && (
        <div className="flex items-center gap-1">
          <span className="text-xs text-gray-500">{files.length} file(s)</span>
          <button
            onClick={() => setFiles([])}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
