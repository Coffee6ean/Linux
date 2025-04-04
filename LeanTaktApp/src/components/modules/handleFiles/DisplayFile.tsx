import { useState } from "react";
import { Trash2 } from "lucide-react"; // Using Lucide for consistent icons

// Import SVG components with proper typing
import { ExcelSVG } from "../../../assets/icons/files/XLSX.svg";
import { PdfSVG } from "../../../assets/icons/files/PDF.svg";
import { ImageSVG } from "../../../assets/icons/files/Image.svg";

interface FileDisplayProps {
  file: File;
  onRemove?: () => void;
  className?: string;
}

export default function DisplayFile({ file, onRemove, className }: FileDisplayProps) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const fileIcons = {
    "application/pdf": <PdfSVG className="file-icon-svg" />,
    "image/jpeg": <ImageSVG className="file-icon-svg" />,
    "image/png": <ImageSVG className="file-icon-svg" />,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": (
      <ExcelSVG className="file-icon-svg" />
    ),
    default: <FileIcon className="file-icon-svg" />,
  };

  function formatFileSize(bytes: number): string {
    if (!bytes) return "0 Bytes";
    const units = ["Bytes", "KB", "MB", "GB"];
    const exponent = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, exponent)).toFixed(1)} ${units[exponent]}`;
  }

  const getFileIcon = () => {
    return fileIcons[file.type as keyof typeof fileIcons] || fileIcons.default;
  };

  const truncateFileName = (name: string, maxLength = 25): string => {
    if (name.length <= maxLength) return name;
    const extensionIndex = name.lastIndexOf(".");
    const extension = extensionIndex > 0 ? name.slice(extensionIndex) : "";
    const baseName = name.slice(0, maxLength - extension.length - 3);
    return `${baseName}...${extension}`;
  };

  const handlePreview = () => {
    try {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      
      // Clean up when component unmounts or file changes
      return () => URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Preview failed:", error);
    }
  };

  return (
    <div className={`file-display ${className}`}>
        <div className="file-icon" onClick={handlePreview}>
            {getFileIcon()}
        </div>
        
        <div className="file-info">
            <div className="file-name" title={file.name}>
                {truncateFileName(file.name)}
            </div>
            <div className="file-size">
                {formatFileSize(file.size)}
            </div>
        </div>
        
        {onRemove && (
            <button 
                onClick={(e) => {
                e.stopPropagation();
                onRemove();
                }} 
                className="remove-button"
                aria-label="Remove file"
            >
                <Trash2 size={16} />
            </button>
        )}
      
      {showPreview && previewUrl && (
        <div className="preview-modal" onClick={() => setShowPreview(false)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
            {file.type.startsWith('image/') ? (
                <img src={previewUrl} alt="Preview" />
            ) : (
                <iframe src={previewUrl} title="Document Preview" />
            )}
            <button 
                className="close-button"
                onClick={() => setShowPreview(false)}
            >
                Close
            </button>
            </div>
        </div>
    )}
    </div>
  );
}

// Fallback file icon component
function FileIcon({ className }: { className?: string }) {
  return (
    <svg className={className} /* ... */>
      {/* Your SVG path here */}
    </svg>
  );
}