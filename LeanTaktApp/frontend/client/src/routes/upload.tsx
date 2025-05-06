import React from "react";
import { useState } from 'react';
import ProcessForm from "@/components/modules/forms/ProcessForm";

function Upload() {
    return (
        <div className="max-w-7xl mx-auto p-6 space-y-8">
            <header className="text-center space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">Project File Processor</h1>
                <p className="text-lg text-gray-600">Demo Version</p>
            </header>
            
            <main className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)]">
                <div className="w-full max-w-2xl">
                <ProcessForm />
                </div>
            </main>
        </div>
    );
}

export default Upload;