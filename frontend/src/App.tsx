import { useState, useEffect } from "react";
import { Toaster, toast } from "react-hot-toast";
import { HTTP_BACKEND_URL } from "./config";
import { CodeGenerationModel } from "./lib/models";

// --- Types ---

type AppStatus = "initializing" | "ready" | "loading" | "error";

interface ModelStatus {
  name: string;
  available: boolean;
}

interface HealthStatus {
  status: "healthy" | "unhealthy";
  ollama_url: string;
  models: ModelStatus[];
}

// --- Main App Component ---

function App() {
  // Component State
  const [description, setDescription] = useState<string>("");
  const [model, setModel] = useState<CodeGenerationModel>(CodeGenerationModel.LLAMA3_2_3B);
  const [generatedHtml, setGeneratedHtml] = useState<string>("");
  const [generatedCss, setGeneratedCss] = useState<string>("");
  const [status, setStatus] = useState<AppStatus>("initializing");
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string>("");

  const isBackendHealthy = health?.status === "healthy";
  const areModelsReady = health?.models.every(m => m.available) ?? false;
  const canGenerate = isBackendHealthy && areModelsReady && status !== "loading";

  // --- Effects ---

  useEffect(() => {
    const checkHealth = async () => {
      setStatus("initializing");
      try {
        const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/health`);
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || "The backend is not reachable.");
        }
        setHealth(data);
        setStatus("ready");
      } catch (err: any) {
        setError(err.message || "An unknown error occurred while checking backend health.");
        setStatus("error");
      }
    };
    checkHealth();
  }, []);

  // --- Event Handlers ---

  const handleGenerate = async () => {
    if (!description.trim()) {
      toast.error("Please enter a description for your website.");
      return;
    }

    setStatus("loading");
    setError("");
    setGeneratedHtml("");
    setGeneratedCss("");
    toast.loading("Generating your website...");

    try {
      const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/generate/html`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description, model_name: model }),
      });

      toast.dismiss();
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `An API error occurred: ${response.statusText}`);
      }

      const data = await response.json();
      setGeneratedHtml(data.html);
      setGeneratedCss(data.css);
      setStatus("ready");
      toast.success("Website generated successfully!");
    } catch (err: any) {
      toast.dismiss();
      setError(err.message || "An unknown error occurred during generation.");
      setStatus("error");
      toast.error(err.message || "Failed to generate website.");
    }
  };

  // --- Render Helpers ---

  const createPreviewHtml = () => {
    if (!generatedHtml) return "";
    return `
      <!DOCTYPE html><html lang="en">
      <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Generated Website</title><style>body{font-family:sans-serif;}${generatedCss}</style></head>
      <body>${generatedHtml}</body></html>`;
  };

  const renderModelStatus = () => {
    if (status === 'initializing') return <p className="text-zinc-400">Checking model status...</p>;
    if (status === 'error' || !health) return null;

    return health.models.map(m => (
      <div key={m.name} className="flex items-center space-x-2">
        {m.available ? (
          <span className="text-green-400">✓</span>
        ) : (
          <span className="text-red-400">✗</span>
        )}
        <span className={m.available ? 'text-zinc-300' : 'text-zinc-500'}>{m.name}</span>
        {!m.available && <span className="text-xs text-red-400">(Not installed in Ollama)</span>}
      </div>
    ));
  }

  // --- Main Render ---

  return (
    <>
      <Toaster position="top-center" />
      <div className="flex h-screen bg-zinc-900 text-white">
        {/* Control Panel */}
        <div className="w-1/3 max-w-lg p-6 flex flex-col space-y-6 overflow-y-auto border-r border-zinc-700">
          <header>
            <h1 className="text-3xl font-bold">Local AI Website Builder</h1>
            <div className="flex items-center space-x-2 mt-2">
              <span className="inline-block px-2 py-1 text-xs font-semibold text-green-200 bg-green-800 rounded-full">
                Local AI Only
              </span>
              <span className="inline-block px-2 py-1 text-xs font-semibold text-zinc-300 bg-zinc-700 rounded-full">
                Offline Mode
              </span>
            </div>
          </header>

          <div className="p-4 bg-zinc-800 rounded-lg border border-zinc-700">
            <h2 className="text-lg font-semibold mb-3">System Status</h2>
            <div className="space-y-2 text-sm">
              <p>Ollama: {isBackendHealthy ?
                <span className="text-green-400">Connected</span> :
                <span className="text-red-400">Disconnected</span>}
              </p>
              {renderModelStatus()}
            </div>
          </div>

          {status === "error" && (
            <div className="p-4 bg-red-900/50 border border-red-700 rounded-lg">
              <h3 className="font-bold text-red-300">System Error</h3>
              <p className="text-red-400 mt-1 text-sm">{error}</p>
              <button onClick={() => window.location.reload()} className="mt-3 text-xs text-zinc-300 underline">
                Click to refresh
              </button>
            </div>
          )}

          <div className="flex-grow space-y-4">
            <div>
              <label htmlFor="description" className="block text-lg font-medium mb-2">Website Description</label>
              <textarea
                id="description"
                rows={6}
                className="w-full p-3 bg-zinc-800 border border-zinc-600 rounded-md focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                placeholder="e.g., A modern landing page for a new SaaS product..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={!canGenerate}
              />
            </div>

            <div>
              <label htmlFor="model" className="block text-lg font-medium mb-2">Choose a Model</label>
              <select
                id="model"
                className="w-full p-3 bg-zinc-800 border border-zinc-600 rounded-md focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                value={model}
                onChange={(e) => setModel(e.target.value as CodeGenerationModel)}
                disabled={!canGenerate}
              >
                {health?.models.filter(m => m.available).map(m => (
                  <option key={m.name} value={m.name}>{m.name}</option>
                ))}
              </select>
            </div>

            <button
              onClick={handleGenerate}
              disabled={!canGenerate}
              className="w-full py-3 px-4 bg-indigo-600 rounded-md text-lg font-semibold hover:bg-indigo-700 disabled:bg-zinc-700 disabled:cursor-not-allowed transition-colors"
            >
              {status === "loading" ? "Generating..." : "Generate Website"}
            </button>
          </div>
        </div>

        {/* Preview Pane */}
        <div className="flex-1 flex flex-col bg-zinc-950">
          <div className="p-4 border-b border-zinc-700">
            <h2 className="text-xl font-semibold">Preview</h2>
          </div>
          <div className="flex-1 bg-white">
            {status === "loading" && <div className="flex items-center justify-center h-full text-zinc-500">Generating...</div>}
            {status !== "loading" && generatedHtml && <iframe title="Preview" className="w-full h-full border-0" srcDoc={createPreviewHtml()} />}
            {status !== "loading" && !generatedHtml && <div className="flex items-center justify-center h-full text-zinc-500 p-8 text-center">
              {status === 'error' ? 'Could not generate website due to an error.' : 'Enter a description and click "Generate" to see the preview.'}
            </div>}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
