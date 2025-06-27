import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Upload as UploadIcon, FileText, CheckCircle, AlertCircle, BarChart3 } from 'lucide-react';
import ProcessForm from "@/components/modules/forms/ProcessForm";

function Upload() {
    const navigate = useNavigate();

    const handleGoBack = () => {
        navigate('/');
    };

    const steps = [
        {
            number: 1,
            title: "Prepare Your Data",
            description: "Ensure your Excel file follows the required format"
        },
        {
            number: 2,
            title: "Upload File",
            description: "Select and upload your structured data file"
        },
        {
            number: 3,
            title: "Process & Analyze",
            description: "Our system will validate and process your data"
        }
    ];

    const requirements = [
        "Excel format (.xlsx or .xls)",
        "Proper date formatting (YYYY-M-DD)",
        "HEX color codes starting with #",
        "No merged cells in the spreadsheet",
        "Clear column headers in first row"
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <button
                                onClick={handleGoBack}
                                className="flex items-center space-x-2 text-gray-600 hover:text-purple-600 transition-colors"
                            >
                                <ArrowLeft className="w-5 h-5" />
                                <span>Back to Home</span>
                            </button>
                        </div>
                        <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                                <BarChart3 className="w-5 h-5 text-white" />
                            </div>
                            <h1 className="text-xl font-semibold text-gray-900">Critical Flow Analysis</h1>
                        </div>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className="bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 text-white py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="flex justify-center mb-6">
                        <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
                            <UploadIcon className="w-8 h-8 text-white" />
                        </div>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold mb-4">
                        Upload Your Project Data
                    </h1>
                    <p className="text-xl text-purple-100 max-w-2xl mx-auto">
                        Submit your structured data file for Critical Flow Analysis processing
                    </p>
                    <div className="mt-8">
                        <span className="bg-purple-500/30 text-purple-100 px-4 py-2 rounded-full text-sm font-medium">
                            Demo Version
                        </span>
                    </div>
                </div>
            </section>

            {/* Process Steps */}
            <section className="py-12 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">Upload Process</h2>
                        <p className="text-gray-600">Follow these simple steps to process your data</p>
                    </div>
                    
                    <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-8">
                        {steps.map((step, index) => (
                            <div key={step.number} className="flex items-center">
                                <div className="flex flex-col items-center text-center max-w-xs">
                                    <div className="w-12 h-12 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold mb-3">
                                        {step.number}
                                    </div>
                                    <h3 className="font-semibold text-gray-900 mb-1">{step.title}</h3>
                                    <p className="text-sm text-gray-600">{step.description}</p>
                                </div>
                                {index < steps.length - 1 && (
                                    <div className="hidden md:block ml-8">
                                        <div className="w-8 h-0.5 bg-purple-200"></div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Main Upload Section */}
            <section className="py-12 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid lg:grid-cols-3 gap-8">
                        {/* Requirements Sidebar */}
                        <div className="lg:col-span-1">
                            <div className="bg-white rounded-xl shadow-sm p-6 sticky top-6">
                                <div className="flex items-center space-x-3 mb-4">
                                    <CheckCircle className="w-6 h-6 text-green-600" />
                                    <h3 className="text-lg font-semibold text-gray-900">File Requirements</h3>
                                </div>
                                <ul className="space-y-3">
                                    {requirements.map((req, index) => (
                                        <li key={index} className="flex items-start space-x-3">
                                            <div className="w-2 h-2 bg-purple-600 rounded-full mt-2 flex-shrink-0"></div>
                                            <span className="text-sm text-gray-600">{req}</span>
                                        </li>
                                    ))}
                                </ul>
                                
                                <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                                    <div className="flex items-start space-x-3">
                                        <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
                                        <div>
                                            <h4 className="text-sm font-medium text-amber-800">Important Note</h4>
                                            <p className="text-sm text-amber-700 mt-1">
                                                Make sure your data follows all formatting guidelines to ensure successful processing.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Upload Form */}
                        <div className="lg:col-span-2">
                            <div className="bg-white rounded-xl shadow-sm">
                                <div className="p-6 border-b border-gray-200">
                                    <div className="flex items-center space-x-3">
                                        <FileText className="w-6 h-6 text-purple-600" />
                                        <div>
                                            <h2 className="text-xl font-semibold text-gray-900">Upload Your File</h2>
                                            <p className="text-gray-600">Select your Excel file to begin processing</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="p-6">
                                    <ProcessForm />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Help Section */}
            <section className="py-12 bg-white">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">Need Help?</h2>
                    <p className="text-gray-600 mb-6">
                        If you're having trouble with your file format or need assistance, 
                        refer to our documentation or contact support.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button 
                            onClick={handleGoBack}
                            className="bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                        >
                            View Guidelines
                        </button>
                        <button className="border-2 border-purple-600 text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-purple-50 transition-colors">
                            Contact Support
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Upload;