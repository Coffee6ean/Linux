import { useRef, useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Card } from "../ui/card";
import { HandPlatter } from "lucide-react";

export default function ExcelFileUpload() {
    const fileInputRef = useRef<HTMLInputElement>(null)
    const [fileName, setFileName] = useState<string>('No file selected')
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setError(null)

        const file = event.target.files?.[0]

        if (!file) {
            setFileName('No file selected')
            return
        }

        if (!file.name.endsWith('.xlsx')) {
            setFileName('')
            setError('Please select an Excel file (.xlsx) only')
            return
          }
          
          setFileName(`Selected: ${file.name}`)
          await processExcelFile(file)
    }

    const processExcelFile = async (file: File) => {
        setIsLoading(true); // Start loading state
        
        try {
        // 1. Prepare the form data payload
        const formData = new FormData();
        formData.append('excel_file', file); // The actual Excel file
        formData.append('sheet_name', 'Sheet1'); // Default worksheet name
    
        // 2. Send to backend
        const response = await fetch('/api/upload-excel', {
            method: 'POST',
            body: formData, // FormData automatically sets Content-Type header
        });
    
        // 3. Handle HTTP errors (404, 500, etc.)
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
    
        // 4. Parse successful response
        const result = await response.json();
        console.log('Upload successful:', result);
        
        } catch (err) {
        // 5. Handle any errors (network or server errors)
        console.error('Error uploading file:', err);
        setError(err instanceof Error ? err.message : 'Failed to process file');
        
        } finally {
        // 6. Cleanup - runs whether success or failure
        setIsLoading(false);
        }
    }

    return (
      <Card className="p-4 max-w-md">
        <div className="space-y-4">
          <Input ref={fileInputRef} type="file" accept=".xlsx" onChange={handleFileChange} className="hidden"/>
          
          <Button type="button" variant="outline" onClick={() => fileInputRef.current?.click()}>
            Select Excel File
          </Button>
          
          <div className="text-sm text-gray-500">
            {fileName}
          </div>
        </div>
      </Card>
    )
}
