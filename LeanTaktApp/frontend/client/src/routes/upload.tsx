import React from "react";
import { useState } from 'react';
import FileUpload from "@/components/modules/handleFiles/FileUpload";

function Upload() {
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const handleFileUpload = (file: File) => {
        setUploadedFile(file);
    };

    const handleRemoveFile = () => {
        setUploadedFile(null);
    };

    return (
        <div>
            <h1>File Upload Demo</h1>
            <FileUpload fileType="xlsx" onUpload={handleFileUpload} />
        </div>
    );
}

export default Upload;