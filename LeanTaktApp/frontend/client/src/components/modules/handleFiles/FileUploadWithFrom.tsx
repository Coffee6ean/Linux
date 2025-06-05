// components/FileUploadWithForm.tsx
import { useState } from "react";
import { DynamicForm } from "../forms/DynamicForm";

export function FileUploadWithForm() {
  // File state
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);

  // Form state
  const [formValues, setFormValues] = useState<Record<string, string>>({});
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [isProcessing, setIsProcessing] = useState(false);

  // Define your form fields in the parent
  const formFields = [
    {
      id: "project_client",
      label: "Client",
      required: true,
      placeholder: "Acme Corp",
    },
    {
      id: "project_name",
      label: "Project Name",
      required: true,
      placeholder: "Website Redesign",
    },
    {
      id: "project_code",
      label: "Project Code",
      placeholder: "PRJ-2023-001",
    },
    // Add all other fields...
  ];

  const handleFileChange = (file: File) => {
    // Your file validation logic
    if (!file.name.endsWith(".xlsx")) {
      setFileError("Only .xlsx files are accepted");
      return;
    }
    setFile(file);
    setFileError(null);
  };

  const handleFormChange = (id: string, value: string) => {
    setFormValues((prev) => ({ ...prev, [id]: value }));
    // Clear error when user types
    setFormErrors((prev) => ({ ...prev, [id]: "" }));
  };

  const validateForm = () => {
    const errors: Record<string, string> = {};
    formFields.forEach((field) => {
      if (field.required && !formValues[field.id]) {
        errors[field.id] = `${field.label} is required`;
      }
    });
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    
    setIsProcessing(true);
    try {
      const formData = new FormData();
      if (file) formData.append("file", file);
      
      // Append all form values
      Object.entries(formValues).forEach(([key, value]) => {
        formData.append(key, value);
      });

      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });
      
      // Handle response...
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Your existing FileUpload component */}
      <div className="p-6 border rounded-lg">
        {/* File upload UI... */}
      </div>

      {/* Conditionally render form */}
      {file && (
        <DynamicForm
          fields={formFields}
          values={formValues}
          errors={formErrors}
          onChange={handleFormChange}
          onSubmit={handleSubmit}
          onCancel={() => setFile(null)}
          submitText="Process File"
          isLoading={isProcessing}
        />
      )}
    </div>
  );
}