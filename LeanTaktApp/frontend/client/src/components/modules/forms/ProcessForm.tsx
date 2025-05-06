import { useState, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { FileType } from "lucide-react";

export default function ProcessForm() {
    //Refs
    const fileInputRef = useRef<HTMLInputElement>(null);

    //States
    const [file, setFile] = useState<File|null>(null);
    const [error, setError] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);

    //Form fields
    const [formData, setFormData] = useState({
        project_client: "",
        project_name: "",
        project_code: "",
        project_title: "",
        project_subtitle: "",
        project_workweek: "",
        project_location: "",
        project_assignee: "",
        project_tags: "",
    });

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        if (!selectedFile.name.endsWith(".xlsx")) {
            setError("Please upload an Excel (.xlsx) file");
            return;
        };

        setFile(selectedFile);
        setError("");
    };
    
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
          ...prev,
          [name as keyof FormData]: value
        }));
    };

    const handleSubmit = async () => {
        if (!file) {
            setError("Please select a file first");
            return;
        }

        setIsProcessing(true);

        try {
            const formPayLoad = new FormData();
            formPayLoad.append("file", file);

            Object.entries(formData).forEach(([key, value]) => {
                formPayLoad.append(key, value)
            });

            const response = await fetch("http://localhost:5000/api/process", {
                method: "POST",
                body: formPayLoad,
            });

            const result = await response.json();
            console.log("Processing result:", result)
        } catch (err) {
            setError("Failed process file");
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <Card>
            <div>
                {/* File Upload Section */}
                <div className="space-y-2">
                    <Label htmlFor="file-upload">Upload Excel File</Label>
                    <Input
                        id="file-upload"
                        type="file"
                        accept=".xlsx"
                        onChange={handleFileChange}
                        ref={fileInputRef}
                        className="hidden"
                    />
                    <div className="flex gap-2">
                        <Button
                            type="button"
                            onClick={() => fileInputRef.current?.click()}
                            variant="outline"
                        > 
                            Select File 
                        </Button>
                        <span className="self-center text-sm">
                            {file ? file.name : "No file Selected"}
                        </span>
                    </div>
                    {error && <p className="text-sm text-red-500">{error}</p>}
                </div>

                {/* Form Fields (shown only after file selection) */}
                {file && (
                    <div className="space-y-3">
                    <div>
                      <Label htmlFor="project_client">Client</Label>
                      <Input
                        id="project_client"
                        name="project_client"
                        value={formData.project_client}
                        onChange={handleInputChange}
                      />
                    </div>
        
                    <div>
                      <Label htmlFor="project_name">Project Name</Label>
                      <Input
                        id="project_name"
                        name="project_name"
                        value={formData.project_name}
                        onChange={handleInputChange}
                      />
                    </div>
        
                    <div>
                      <Label htmlFor="project_code">Project Code</Label>
                      <Input
                        id="project_code"
                        name="project_code"
                        value={formData.project_code}
                        onChange={handleInputChange}
                      />
                    </div>
        
                    {/* Add other fields as needed */}
                  </div>
                )}

                {/* Submit Button */}
                <Button
                    onClick={handleSubmit}
                    disabled={!file || isProcessing}
                    className="w-full"
                >
                    {isProcessing ? 'Processing...' : 'Process File'}
                </Button>
            </div>
        </Card>
    )
}