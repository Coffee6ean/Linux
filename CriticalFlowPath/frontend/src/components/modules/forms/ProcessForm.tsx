import { useState, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import config from '../../../config';

export default function ProcessForm() { 
  //Refs
  const fileInputRef = useRef<HTMLInputElement>(null);

  //States
  const [file, setFile] = useState<File|null>(null);
  const [error, setError] = useState("");
  const [formErrors, setFormErrors] = useState({});
  const [isProcessing, setIsProcessing] = useState(false);

  // Week Days
  const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  //Form fields
  const [formData, setFormData] = useState({
    project_client: '',
    project_name: '',
    project_code: '',
    project_title: '',
    project_subtitle: '', // Optional
    project_workweek_start: '',
    project_workweek_finish: '',
    project_location: '', // Optional
    project_assignee: '',
    project_tags: '' // Optional
  });

  // Required fields (excluding optional ones)
  const requiredFields = [
    'project_client',
    'project_name', 
    'project_code',
    'project_title',
    'project_workweek_start',
    'project_workweek_finish',
    'project_assignee'
  ];

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

      // Clear error for this field when user starts typing
      if (formErrors[name]) {
        setFormErrors(prev => ({
            ...prev,
            [name]: ''
        }));
    }
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({
        ...prev,
        [name]: value
    }));
    
    // Clear error for this field when user selects
    if (formErrors[name]) {
        setFormErrors(prev => ({
            ...prev,
            [name]: ''
        }));
    }
  };

  const validateForm = () => {
    const errors = {};
    
    // Check required fields
    requiredFields.forEach(field => {
        if (!formData[field] || formData[field].trim() === '') {
            errors[field] = 'This field is required';
        }
    });

    // Validate workweek logic
    if (formData.project_workweek_start && formData.project_workweek_finish) {
        const startIndex = weekdays.indexOf(formData.project_workweek_start);
        const endIndex = weekdays.indexOf(formData.project_workweek_finish);
        
        if (startIndex > endIndex) {
            errors.project_workweek_finish = 'End day must be after or same as start day';
        }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    if (!validateForm()) {
      setError('Please fill in all required fields');
      return;
    }
  
    setIsProcessing(true);
    setError("");
  
    try {
      const formPayLoad = new FormData();
      formPayLoad.append("file", file);
      formPayLoad.append("config", JSON.stringify(formData));
  
      const response = await fetch(`${config.API_BASE_URL}/execute-cfa-cycle`, {
        method: "POST",
        body: formPayLoad,
      });
  
      if (!response.ok) {
        const err = await response.json();
        console.error("Error:", err);
        return;
      }
  
      // Get filename from content-disposition header
      const disposition = response.headers.get("Content-Disposition");
      let filename = "result.zip";

      if (disposition && disposition.indexOf("attachment") !== -1) {
        const filenameRegex = /file_name[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, "");
        }
      }
  
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);  // use actual filename here
      document.body.appendChild(link);
      link.click();
      link.remove();
  
    } catch (err) {
      setError("Failed to process file");
    } finally {
      setIsProcessing(false);
    }
  };
    
  return (
    <Card className="p-6">
        <div className="space-y-6">
            {/* File Upload Section */}
            <div className="space-y-3">
                <Label htmlFor="file_name" className="text-base font-semibold">
                    Upload Excel File <span className="text-red-500">*</span>
                </Label>
                <Input
                    id="file_name"
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    className="hidden"
                />
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-400 transition-colors">
                    <div className="space-y-2">
                        <Button
                            type="button"
                            onClick={() => fileInputRef.current?.click()}
                            variant="outline"
                            className="border-purple-600 text-purple-600 hover:bg-purple-50"
                        > 
                            Choose File
                        </Button>
                        <p className="text-sm text-gray-600">
                            {file ? (
                                <span className="text-green-600 font-medium">✓ {file.name}</span>
                            ) : (
                                "Select your Excel file (.xlsx or .xls)"
                            )}
                        </p>
                    </div>
                </div>
                {error && <p className="text-sm text-red-500">{error}</p>}
            </div>

            {/* Form Fields (shown only after file selection) */}
            {file && (
                <div className="space-y-4">
                    <div className="border-t pt-6">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Information</h3>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Client - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_client">
                                    Client <span className="text-red-500">*</span>
                                </Label>
                                <Input
                                    id="project_client"
                                    name="project_client"
                                    value={formData.project_client}
                                    onChange={handleInputChange}
                                    className={formErrors.project_client ? 'border-red-500' : ''}
                                    placeholder="Enter client name"
                                />
                                {formErrors.project_client && (
                                    <p className="text-sm text-red-500">{formErrors.project_client}</p>
                                )}
                            </div>

                            {/* Project Name - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_name">
                                    Project Name <span className="text-red-500">*</span>
                                </Label>
                                <Input
                                    id="project_name"
                                    name="project_name"
                                    value={formData.project_name}
                                    onChange={handleInputChange}
                                    className={formErrors.project_name ? 'border-red-500' : ''}
                                    placeholder="Enter project name"
                                />
                                {formErrors.project_name && (
                                    <p className="text-sm text-red-500">{formErrors.project_name}</p>
                                )}
                            </div>

                            {/* Project Code - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_code">
                                    Project Code <span className="text-red-500">*</span>
                                </Label>
                                <Input
                                    id="project_code"
                                    name="project_code"
                                    value={formData.project_code}
                                    onChange={handleInputChange}
                                    className={formErrors.project_code ? 'border-red-500' : ''}
                                    placeholder="Enter project code"
                                />
                                {formErrors.project_code && (
                                    <p className="text-sm text-red-500">{formErrors.project_code}</p>
                                )}
                            </div>

                            {/* Project Title - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_title">
                                    Project Title <span className="text-red-500">*</span>
                                </Label>
                                <Input
                                    id="project_title"
                                    name="project_title"
                                    value={formData.project_title}
                                    onChange={handleInputChange}
                                    className={formErrors.project_title ? 'border-red-500' : ''}
                                    placeholder="Enter project title"
                                />
                                {formErrors.project_title && (
                                    <p className="text-sm text-red-500">{formErrors.project_title}</p>
                                )}
                            </div>

                            {/* Project Subtitle - Optional */}
                            <div className="space-y-2 md:col-span-2">
                                <Label htmlFor="project_subtitle">
                                    Project Subtitle <span className="text-gray-400">(Optional)</span>
                                </Label>
                                <Input
                                    id="project_subtitle"
                                    name="project_subtitle"
                                    value={formData.project_subtitle}
                                    onChange={handleInputChange}
                                    placeholder="Enter project subtitle (optional)"
                                />
                            </div>

                            {/* Workweek Start - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_workweek_start">
                                    Workweek Start <span className="text-red-500">*</span>
                                </Label>
                                <Select
                                    value={formData.project_workweek_start}
                                    onValueChange={(value) => handleSelectChange('project_workweek_start', value)}
                                >
                                    <SelectTrigger className={formErrors.project_workweek_start ? 'border-red-500' : ''}>
                                        <SelectValue placeholder="Select start day" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {weekdays.map((day) => (
                                            <SelectItem key={day} value={day}>
                                                {day}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                                {formErrors.project_workweek_start && (
                                    <p className="text-sm text-red-500">{formErrors.project_workweek_start}</p>
                                )}
                            </div>

                            {/* Workweek End - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_workweek_finish">
                                    Workweek End <span className="text-red-500">*</span>
                                </Label>
                                <Select
                                    value={formData.project_workweek_finish}
                                    onValueChange={(value) => handleSelectChange('project_workweek_finish', value)}
                                >
                                    <SelectTrigger className={formErrors.project_workweek_finish ? 'border-red-500' : ''}>
                                        <SelectValue placeholder="Select end day" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {weekdays.map((day) => (
                                            <SelectItem key={day} value={day}>
                                                {day}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                                {formErrors.project_workweek_finish && (
                                    <p className="text-sm text-red-500">{formErrors.project_workweek_finish}</p>
                                )}
                            </div>

                            {/* Project Location - Optional */}
                            <div className="space-y-2">
                                <Label htmlFor="project_location">
                                    Project Location <span className="text-gray-400">(Optional)</span>
                                </Label>
                                <Input
                                    id="project_location"
                                    name="project_location"
                                    value={formData.project_location}
                                    onChange={handleInputChange}
                                    placeholder="Enter project location (optional)"
                                />
                            </div>

                            {/* Project Assignee - Required */}
                            <div className="space-y-2">
                                <Label htmlFor="project_assignee">
                                    Project Assignee <span className="text-red-500">*</span>
                                </Label>
                                <Input
                                    id="project_assignee"
                                    name="project_assignee"
                                    value={formData.project_assignee}
                                    onChange={handleInputChange}
                                    className={formErrors.project_assignee ? 'border-red-500' : ''}
                                    placeholder="Enter assignee name"
                                />
                                {formErrors.project_assignee && (
                                    <p className="text-sm text-red-500">{formErrors.project_assignee}</p>
                                )}
                            </div>

                            {/* Project Tags - Optional */}
                            <div className="space-y-2 md:col-span-2">
                                <Label htmlFor="project_tags">
                                    Project Tags <span className="text-gray-400">(Optional)</span>
                                </Label>
                                <Input
                                    id="project_tags"
                                    name="project_tags"
                                    value={formData.project_tags}
                                    onChange={handleInputChange}
                                    placeholder="Enter tags separated by commas (optional)"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Submit Button */}
            <Button
                onClick={handleSubmit}
                disabled={!file || isProcessing}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3"
            >
                {isProcessing ? 'Processing...' : 'Process File'}
            </Button>
        </div>
    </Card>
  );
}