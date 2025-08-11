import { useState, useEffect } from "react";
import { Toaster, toast } from "react-hot-toast";
import { HTTP_BACKEND_URL } from "./config";
import { CodeGenerationModel } from "./lib/models"; // Using existing model definitions

// Simplified component state
type AppStatus = "initial" | "loading" | "ready" | "error";

function App() {
  const [description, setDescription] = useState<string>("");
  const [model, setModel] = useState<CodeGenerationModel>(CodeGenerationModel.LLAMA3_2_3B);
  const [generatedHtml, setGeneratedHtml] = useState<string>("");
  const [generatedCss, setGeneratedCss] = useState<string>("");
  const [status, setStatus] = useState<AppStatus>("initial");
  const [error, setError] = useState<string>("");
  const [backendHealth, setBackendHealth] = useState<boolean | null>(null);

  // Check backend health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/health`);
        if (response.ok) {
          const data = await response.json();
          setBackendHealth(data.status === "healthy");
        } else {
          setBackendHealth(false);
        }
      } catch (err) {
        setBackendHealth(false);
      }
    };
    checkHealth();
  }, []);

  // Function to construct the preview HTML
  const createPreviewHtml = () => {
    if (!generatedHtml) return "";
    return `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Website</title>
        <style>
          body { font-family: sans-serif; }
          ${generatedCss}
        </style>
      </head>
      <body>
        ${generatedHtml}
      </body>
      </html>
    `;
  };

  const handleGenerate = async () => {
    if (!description.trim()) {
      toast.error("Please enter a description for your website.");
      return;
    }

    setStatus("loading");
    setError("");
    setGeneratedHtml("");
    setGeneratedCss("");

    try {
      const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/generate/html`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: description,
          model_name: model,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setGeneratedHtml(data.html);
      setGeneratedCss(data.css);
      setStatus("ready");
      toast.success("Website generated successfully!");
    } catch (err: any) {
      setError(err.message || "An unknown error occurred.");
      setStatus("error");
      toast.error(err.message || "Failed to generate website.");
    }
  };

  return (
    <>
      <Toaster position="top-center" />
      <div className="flex h-screen bg-zinc-900 text-white">
        {/* Control Panel */}
        <div className="w-1/3 max-w-lg p-6 space-y-6 overflow-y-auto border-r border-zinc-700">
          <header>
            <h1 className="text-3xl font-bold">Local AI Website Builder</h1>
            <p className="text-zinc-400 mt-2">
              Describe the website you want to create, and let a local Ollama model build it for you.
            </p>
            <div className="text-xs mt-3">
              Backend status: {backendHealth === null ? "checking..." : backendHealth ?
              <span className="text-green-400">connected</span> :
              <span className="text-red-400">disconnected</span>}
            </div>
          </header>

          <div className="space-y-4">
            {/* Prompt Input */}
            <div>
              <label htmlFor="description" className="block text-lg font-medium mb-2">
                Website Description
              </label>
              <textarea
                id="description"
                rows={6}
                className="w-full p-3 bg-zinc-800 border border-zinc-600 rounded-md focus:ring-2 focus:ring-indigo-500"
                placeholder="e.g., A modern landing page for a new SaaS product..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            {/* Model Selection */}
            <div>
              <label htmlFor="model" className="block text-lg font-medium mb-2">
                Choose a Model
              </label>
              <select
                id="model"
                className="w-full p-3 bg-zinc-800 border border-zinc-600 rounded-md focus:ring-2 focus:ring-indigo-500"
                value={model}
                onChange={(e) => setModel(e.target.value as CodeGenerationModel)}
              >
                <option value={CodeGenerationModel.GPT_OSS_20B}>gpt-oss-20b</option>
                <option value={CodeGenerationModel.LLAMA3_2_3B}>llama3.2:3b</option>
              </select>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={status === "loading" || !backendHealth}
              className="w-full py-3 px-4 bg-indigo-600 rounded-md text-lg font-semibold hover:bg-indigo-700 disabled:bg-zinc-700 disabled:cursor-not-allowed transition-colors"
            >
              {status === "loading" ? "Generating..." : "Generate Website"}
            </button>
          </div>

          {status === "error" && (
            <div className="p-4 bg-red-900 border border-red-700 rounded-md">
              <h3 className="font-bold text-red-300">Error</h3>
              <p className="text-red-400 mt-1">{error}</p>
            </div>
          )}
        </div>

        {/* Preview Pane */}
        <div className="flex-1 flex flex-col bg-zinc-950">
          <div className="p-4 border-b border-zinc-700">
            <h2 className="text-xl font-semibold">Preview</h2>
          </div>
          <div className="flex-1 bg-white">
            {status === "initial" && (
              <div className="flex items-center justify-center h-full text-zinc-500">
                Enter a description and click "Generate" to see the preview.
              </div>
            )}
            {status === "loading" && (
              <div className="flex items-center justify-center h-full text-zinc-500">
                <p>Generating your website...</p>
              </div>
            )}
            {status === "ready" && (
              <iframe
                title="Generated Website Preview"
                className="w-full h-full border-0"
                srcDoc={createPreviewHtml()}
              />
            )}
            {status === "error" && (
               <div className="flex items-center justify-center h-full text-red-500">
                <p>Could not generate website due to an error.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
