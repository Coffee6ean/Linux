import { useState } from 'react';
import FileUpload from './components/modules/handleFiles/FileUpload';
import './App.css';

function App() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
  };

  const handleRemoveFile = () => {
    setUploadedFile(null);
  };

  return (
    <div className="app-container">
      <h1>File Upload Demo</h1>
      
      <FileUpload fileType="xlsx" onUpload={handleFileUpload} />
    </div>
  );
}

export default App;
