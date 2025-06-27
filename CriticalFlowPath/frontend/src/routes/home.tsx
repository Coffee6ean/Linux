import { useNavigate } from 'react-router-dom';
import { ChevronRight, FileText, Database, Settings, CheckCircle, Calendar, Users, BarChart3 } from 'lucide-react';

export default function CFAProcessPage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/upload');
  };

  const steps = [
    {
      id: 1,
      title: "Data Preparation",
      description: "Submit structured data files that the Critical Flow Analysis program can efficiently process",
      icon: <FileText className="w-6 h-6" />,
      details: [
        "All data entries must be in recognized data format within Excel",
        "Dates should align with YYYY-M-DD standard format", 
        "Example: 01-Jan-2024 for the first day"
      ]
    },
    {
      id: 2,
      title: "File Formatting",
      description: "Ensure proper file structure and formatting guidelines are followed",
      icon: <Database className="w-6 h-6" />,
      details: [
        "All color codes must be specified in HEX format",
        "Each color code should begin with # followed by six hexadecimal digits",
        "Submit structured data files in Excel format (XLSX)"
      ]
    },
    {
      id: 3,
      title: "Activity Configuration", 
      description: "Define activity codes, names, and category structures for your project",
      icon: <Settings className="w-6 h-6" />,
      details: [
        "Each entry must include unique code and descriptive name",
        "Activities should be logical and concise with clear names",
        "Each entry should belong to a defined category"
      ]
    },
    {
      id: 4,
      title: "Validation & Processing",
      description: "System validates data and processes it through the CFA algorithm",
      icon: <CheckCircle className="w-6 h-6" />,
      details: [
        "Perform validation checks on all required fields", 
        "Ensure data is populated and correctly formatted",
        "Double-check for missing or incorrect entries"
      ]
    }
  ];

  const features = [
    {
      icon: <Calendar className="w-8 h-8 text-purple-600" />,
      title: "Schedule Optimization",
      description: "Transform well-structured data files into organized schedules and legends that adhere to the CFA style"
    },
    {
      icon: <Users className="w-8 h-8 text-purple-600" />,
      title: "Project Management",
      description: "Designed for departmental staff who interact with Critical Flow Analysis for submitting data"
    },
    {
      icon: <BarChart3 className="w-8 h-8 text-purple-600" />,
      title: "Analysis & Reporting",
      description: "Generate comprehensive reports and visualizations for project tracking and analysis"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-xl font-semibold text-gray-900">Critical Flow Analysis</h1>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#process" className="text-gray-600 hover:text-purple-600 transition-colors">Process</a>
              <a href="#features" className="text-gray-600 hover:text-purple-600 transition-colors">Features</a>
              <a href="#guidelines" className="text-gray-600 hover:text-purple-600 transition-colors">Guidelines</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Critical Flow Analysis
            </h1>
            <p className="text-xl md:text-2xl text-purple-100 mb-8 max-w-3xl mx-auto">
              Streamline your project management with structured data analysis and automated schedule generation
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={handleGetStarted}
                className="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Get Started
              </button>
              <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors">
                View Documentation
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Process Steps */}
      <section id="process" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Step-by-Step Submission Process
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Follow these key components to ensure successful data submission and processing
            </p>
          </div>

          <div className="grid gap-8 md:gap-12">
            {steps.map((step, index) => (
              <div key={step.id} className="flex flex-col lg:flex-row items-start gap-8">
                <div className="flex-shrink-0">
                  <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
                    <div className="text-purple-600">
                      {step.icon}
                    </div>
                  </div>
                </div>
                
                <div className="flex-grow">
                  <div className="flex items-center gap-4 mb-4">
                    <span className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                      Step {step.id}
                    </span>
                    <h3 className="text-2xl font-bold text-gray-900">{step.title}</h3>
                  </div>
                  
                  <p className="text-lg text-gray-600 mb-6">{step.description}</p>
                  
                  <div className="bg-gray-50 rounded-lg p-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Key Requirements:</h4>
                    <ul className="space-y-2">
                      {step.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start gap-3">
                          <ChevronRight className="w-5 h-5 text-purple-600 flex-shrink-0 mt-0.5" />
                          <span className="text-gray-700">{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                
                {index < steps.length - 1 && (
                  <div className="hidden lg:block w-8 flex-shrink-0">
                    <div className="w-full h-24 flex items-center justify-center">
                      <div className="w-0.5 h-full bg-purple-200"></div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Key Features
            </h2>
            <p className="text-xl text-gray-600">
              Powerful tools designed to enhance project processing efficiency
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow">
                <div className="mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Guidelines Section */}
      <section id="guidelines" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl p-8 md:p-12">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Data Submission Guidelines
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Our goal is to create a seamless pipeline for data transfer that supports informed decision-making 
                throughout the lifecycle of construction projects.
              </p>
              
              <div className="grid md:grid-cols-2 gap-8 text-left">
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-bold text-gray-900 mb-3">📊 Data Format</h3>
                  <p className="text-gray-600 text-sm">
                    Use clear and descriptive headers for each column such as "Start Date", 
                    "Activity Name", "Activity Code", and "Activity Name"
                  </p>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-bold text-gray-900 mb-3">🔍 Validation Checks</h3>
                  <p className="text-gray-600 text-sm">
                    Before submitting, perform validation checks to ensure all required fields 
                    are populated and correctly formatted
                  </p>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-bold text-gray-900 mb-3">📋 Column Headers</h3>
                  <p className="text-gray-600 text-sm">
                    Ensure that headers are placed in the first row of your Excel sheet 
                    and follow the specified naming conventions
                  </p>
                </div>
                
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-bold text-gray-900 mb-3">⚠️ Avoid Merged Cells</h3>
                  <p className="text-gray-600 text-sm">
                    Do not use merged cells in your Excel file as they can lead to processing 
                    errors in the Critical Flow Analysis program
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-semibold">Critical Flow Analysis</span>
            </div>
            <p className="text-gray-400">
              Streamlining project management through structured data analysis
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}