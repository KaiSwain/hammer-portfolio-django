"use client";

import { useEffect, useState } from "react";
import { apiService } from "@/app/services/api";

/**
 * StudentFiles Component
 * --------------------------
 * Displays student files and provides upload/download/delete functionality
 * Features:
 * - File list with download and delete options
 * - Drag and drop file upload
 * - PDF-only validation with 25MB size limit
 * - File size display in MB
 */
export default function StudentFiles({ studentId, studentName = "Student" }) {
  const [files, setFiles] = useState([]); // Always initialize as empty array
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState(null);

  // Fetch student files on component mount
  useEffect(() => {
    loadStudentFiles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [studentId]);

  const loadStudentFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await apiService.getStudentFiles(studentId);
      console.log("Student files loaded successfully:", data);
      
      // The API service now ensures data is always an array
      setFiles(data);
    } catch (err) {
      console.error("Error loading student files:", err);
      
      if (err.message === 'Authentication required') {
        setError("Please log in to view student files");
      } else {
        setError("Failed to load student files");
      }
      
      setFiles([]); // Always ensure files is an array
    } finally {
      setLoading(false);
    }
  };

  const validateFile = (file) => {
    // Check file size (100MB limit)
    const maxSize = 100 * 1024 * 1024; // 100MB in bytes
    if (file.size > maxSize) {
      throw new Error('File size must be less than 100MB');
    }
    
    // Security: Block potentially dangerous file extensions
    const dangerousExtensions = ['.exe', '.bat', '.cmd', '.scr', '.pif', '.com', '.vbs', '.js'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    if (dangerousExtensions.includes(fileExtension)) {
      throw new Error('File type not allowed for security reasons');
    }
  };

  const handleFileUpload = async (files) => {
    const fileArray = Array.isArray(files) ? files : [files];
    
    try {
      setUploading(true);
      setError(null);
      
      let successCount = 0;
      let errorCount = 0;
      const errors = [];
      
      for (const file of fileArray) {
        try {
          validateFile(file);
          
          await apiService.uploadStudentFile(
            studentId,
            file,
            file.name
          );
          
          successCount++;
        } catch (err) {
          errorCount++;
          errors.push(`${file.name}: ${err.message}`);
        }
      }
      
      // Refresh file list
      await loadStudentFiles();
      
      if (successCount > 0) {
        console.log(`${successCount} file(s) uploaded successfully`);
      }
      
      if (errorCount > 0) {
        setError(`${errorCount} file(s) failed to upload:\n${errors.slice(0, 3).join('\n')}${errors.length > 3 ? '\n...' : ''}`);
      }
      
    } catch (err) {
      console.error("File upload error:", err);
      setError(err.message || "Failed to upload files");
    } finally {
      setUploading(false);
    }
  };

  const handleFileDelete = async (fileId, fileName) => {
    if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
      return;
    }

    try {
      await apiService.deleteStudentFile(fileId);
      await loadStudentFiles(); // Refresh list
    } catch (err) {
      console.error("File delete error:", err);
      setError("Failed to delete file");
    }
  };

  const handleFileDownload = async (fileId, fileName) => {
    try {
      const downloadData = await apiService.downloadStudentFile(fileId);
      const blob = await downloadData.response.blob();
      
      // Use the filename from the API response for accuracy
      const actualFileName = downloadData.filename || fileName;
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = actualFileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      console.log(`File downloaded: ${actualFileName}`);
    } catch (err) {
      console.error("File download error:", err);
      setError("Failed to download file");
    }
  };

  // Drag and drop handlers
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length > 0) {
      handleFileUpload(droppedFiles);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
      handleFileUpload(selectedFiles);
    }
    e.target.value = ''; // Reset input
  };

  const formatFileSize = (sizeInBytes) => {
    const sizeInMB = sizeInBytes / (1024 * 1024);
    return `${sizeInMB.toFixed(2)} MB`;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getFileIcon = (filename, contentType) => {
    const extension = filename.toLowerCase().split('.').pop();
    
    // Image files
    if (contentType?.startsWith('image/') || ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'].includes(extension)) {
      return '🖼️';
    }
    
    // Video files
    if (contentType?.startsWith('video/') || ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'].includes(extension)) {
      return '🎥';
    }
    
    // Audio files
    if (contentType?.startsWith('audio/') || ['mp3', 'wav', 'ogg', 'flac', 'm4a'].includes(extension)) {
      return '🎵';
    }
    
    // Document files
    if (['pdf'].includes(extension)) return '📄';
    if (['doc', 'docx'].includes(extension)) return '📝';
    if (['xls', 'xlsx'].includes(extension)) return '📊';
    if (['ppt', 'pptx'].includes(extension)) return '📋';
    if (['txt', 'md'].includes(extension)) return '📃';
    
    // Archive files
    if (['zip', 'rar', '7z', 'tar', 'gz'].includes(extension)) return '📦';
    
    // Code files
    if (['js', 'ts', 'py', 'java', 'cpp', 'c', 'html', 'css', 'php'].includes(extension)) return '⚡';
    
    // Default file icon
    return '📁';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        📁 {studentName} Files
      </h3>

      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-6 mb-6 transition-colors ${
          dragOver
            ? "border-blue-400 bg-blue-50"
            : uploading
            ? "border-gray-300 bg-gray-50"
            : "border-gray-300 hover:border-gray-400"
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="text-center">
          {uploading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600">Uploading...</span>
            </div>
          ) : (
            <>
              <div className="text-gray-600 mb-2">
                � Drag and drop any files here, or{" "}
                <label className="text-blue-600 hover:text-blue-800 cursor-pointer underline">
                  browse files
                  <input
                    type="file"
                    onChange={handleFileSelect}
                    className="hidden"
                    multiple
                  />
                </label>
                {" | "}
                <label className="text-blue-600 hover:text-blue-800 cursor-pointer underline">
                  browse folders
                  <input
                    type="file"
                    webkitdirectory="true"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                </label>
              </div>
              <div className="text-sm text-gray-500">
                All file types accepted, maximum 100MB per file
              </div>
            </>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Files List */}
      <div>
        <h4 className="font-medium text-gray-800 mb-3">Uploaded Files</h4>
        
        {loading ? (
          <div className="text-center py-4">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
            <span className="text-gray-600 mt-2 block">Loading files...</span>
          </div>
        ) : !Array.isArray(files) || files.length === 0 ? (
          <div className="text-gray-500 text-center py-4">
            No files uploaded yet
          </div>
        ) : (
          <div className="space-y-2">
            {files.map((file) => (
              <div
                key={file.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded border"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center">
                    <span className="mr-2">{getFileIcon(file.original_filename, file.content_type)}</span>
                    <span className="font-medium text-gray-800 truncate">
                      {file.original_filename}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 mt-1">
                    {formatFileSize(file.file_size)} • Uploaded {formatDate(file.uploaded_at)}
                    {file.uploaded_by_name && ` by ${file.uploaded_by_name}`}
                  </div>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <button
                    onClick={() => handleFileDownload(file.id, file.original_filename)}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    title="Download file"
                  >
                    Download
                  </button>
                  <button
                    onClick={() => handleFileDelete(file.id, file.original_filename)}
                    className="text-red-600 hover:text-red-800 text-sm font-medium"
                    title="Delete file"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}