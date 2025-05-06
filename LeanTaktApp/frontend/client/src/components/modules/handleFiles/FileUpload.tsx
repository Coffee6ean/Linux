// components/modules/FileUpload.tsx
import { useRef, useState } from "react";
import { DynamicForm } from "../forms/DynamicForm";

import { Button } from "../../ui/button";
import { Input } from "../../ui/input";
import { Card } from "../../ui/card";
import { Loader2 } from "lucide-react";

type FileType = 'xlsx' | 'pdf' | 'csv' | 'image';

interface FileUploadProps {
  fileType: string;
  onUpload: (file: File) => void;
  disabled?: boolean;
}

export default function FileUpload({ fileType, onUpload, disabled }: FileUploadProps) {
  //File state
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string>('No file selected');
  const [isLoading, setIsLoading] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [fileUploaded, setFileUploaded] = useState(false);

  const getAcceptString = () => {
    const typeMap = {
      xlsx: '.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      pdf: '.pdf, application/pdf',
      csv: '.csv, text/csv',
      image: 'image/*'
    };
    return typeMap[fileType];
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    setFileError(null);
    setFileUploaded(false);
    const file = event.target.files?.[0];
    
    if (!file) {
      setFileName('No file selected');
      return;
    }

    const validExtensions = {
      xlsx: ['.xlsx'],
      pdf: ['.pdf'],
      csv: ['.csv'],
      image: ['.jpg', '.jpeg', '.png', '.gif']
    };

    const isValidExtension = validExtensions[fileType].some(ext => 
      file.name.toLowerCase().endsWith(ext)
    );

    if (!isValidExtension) {
      setFileName('');
      setFileError(`Please select a valid ${fileType} file`);
      return;
    }

    setFileName(`Selected: ${file.name}`);
    setIsLoading(true);
    
    try {
      await onUpload(file);
      setFileUploaded(true);
    } catch (err) {
      setFileError(err instanceof Error ? err.message : 'Failed to process file');
      setFileUploaded(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProcessClick = async () => {
    if (!fileUploaded || isLoading) return;

    setIsLoading(true)

    try {
      const response = await fetch("http://localhost:5000/api/process", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          test: "Hello World"
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP fileError! status: ${response.status}`);
      }

      const data = await response.json();
      setResponseData(data)
      console.log("Processing successful:", data);
    } catch (fileError) {
      setResponseData(fileError)
      console.fileError("Error processing file:", fileError);
    } finally {
      setIsLoading(false)
    };
  };

  //Form state
  const [formValue, setFormValues] = useState<Record<string, string>>({});
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [isProcessing, setIsProcessing] = useState(false);

  const FormFields = [
    {
      id: "project_client",
      label: "Client",
      required: true,
      placeholder: "Placeholder",
    },
    {
      id: "project_name",
      label: "Project Name",
      required: true,
      placeholder: "Placeholder",
    },
    {
      id: "project_code",
      label: "Project Code",
      placeholder: "Placeholder",
    },
  ]

  const handleFileChange = (file:File) => {
    if (!file.name.endsWith()) {
      if (!file.name.endsWith(".xlsx")) {
        setFileError("Only .xlsx files are accepted");
        return;
      }
      setFile(file);
      setFileError(null);
    }
  }

  const [responseData, setResponseData] = useState(null);

  return (
    <Card className="p-6 max-w-md bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="space-y-4">
        {/* Hidden file input */}
        <Input 
          ref={fileInputRef} 
          type="file" 
          accept={getAcceptString()} 
          onChange={handleFileUpload} 
          className="hidden" 
        />
        
        {/* File status display */}
        <div className="space-y-2">
          <h2 className="text-lg font-medium text-gray-800">Upload {fileType} File</h2>
          
          <div className={`p-3 rounded-md border transition-colors ${
            fileError ? 'border-red-200 bg-red-50' : 
            fileUploaded ? 'border-green-200 bg-green-50' : 
            'border-gray-200 bg-gray-50'
          }`}>
            <div className="flex items-center gap-2">
              {fileUploaded ? (
                <div className="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center">
                  <svg className="w-4 h-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              ) : isLoading ? (
                <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
              ) : (
                <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              )}
              
              <span className={`text-sm truncate ${
                fileError ? 'text-red-600' : 
                fileUploaded ? 'text-green-600' : 
                'text-gray-600'
              }`}>
                {fileName}
              </span>
            </div>
            
            {fileError && (
              <div className="flex items-center gap-1 mt-1">
                <svg className="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm text-red-600">{fileError}</span>
              </div>
            )}
          </div>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-3">
          {/* Upload Button */}
          <Button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading || disabled}
            className={`flex-1 ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Uploading...
              </>
            ) : (
              <>
                <svg className="mr-2 w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Select File
              </>
            )}
          </Button>
          
          {/* Process Button */}
          <Button 
            disabled={!fileUploaded || isLoading}
            onClick={handleProcessClick}
            className={`flex-1 transition-colors ${
              fileUploaded 
                ? 'bg-green-600 hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2' 
                : 'bg-gray-200 text-gray-500 cursor-not-allowed'
            }`}
          >
            <svg className="mr-2 w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Process
          </Button>
        </div>
        <div className="mt-4 p-4 bg-green-50 rounded-md">
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      </div>
    </Card>
  );
}
