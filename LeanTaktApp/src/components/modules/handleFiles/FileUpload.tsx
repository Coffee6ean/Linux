// components/modules/FileUpload.tsx
import { useRef, useState } from "react";
import { Button } from "../../ui/button";
import { Input } from "../../ui/input";
import { Card } from "../../ui/card";
import { Loader2 } from "lucide-react";

type FileType = 'xlsx' | 'pdf' | 'csv' | 'image';

interface FileUploadProps {
  fileType: FileType;
  onUpload: (file: File) => Promise<void>;
}

export default function FileUpload({ fileType, onUpload }: FileUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState<string>('No file selected');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getAcceptString = () => {
    const typeMap = {
      xlsx: '.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      pdf: '.pdf, application/pdf',
      csv: '.csv, text/csv',
      image: 'image/*'
    };
    return typeMap[fileType];
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
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
      setError(`Please select a valid ${fileType.toUpperCase()} file`);
      return;
    }

    setFileName(`Selected: ${file.name}`);
    setIsLoading(true);
    
    try {
      await onUpload(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process file');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="p-4 max-w-md">
      <div className="space-y-4">
        <Input ref={fileInputRef} type="file" accept={getAcceptString()} onChange={handleFileChange} className="hidden" />
        <Button type="button" onClick={() => fileInputRef.current?.click()} disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Uploading...
            </>
          ) : `Upload ${fileType.toUpperCase()} File`}
        </Button>
        
        {fileName && (
          <div className="text-sm">{fileName}</div>
        )}
        
        {error && (
          <div className="text-sm text-red-500">{error}</div>
        )}
      </div>
    </Card>
  );
}
