import toast from "react-hot-toast";
import { WS_BACKEND_URL, HTTP_BACKEND_URL } from "./config";
import { FullGenerationSettings } from "./types";

const ERROR_MESSAGE = "Error generating code. Check the console for details.";

type WebSocketResponse = {
  type: "status" | "complete" | "error";
  message?: string;
  data?: {
    html?: string;
    css?: string;
    react?: string;
    enhanced_code?: string;
    fixed_code?: string;
  };
};

interface CodeGenerationCallbacks {
  onChange: (chunk: string, variantIndex: number) => void;
  onSetCode: (code: string, variantIndex: number) => void;
  onStatusUpdate: (status: string, variantIndex: number) => void;
  onVariantComplete: (variantIndex: number) => void;
  onVariantError: (variantIndex: number, error: string) => void;
  onVariantCount: (count: number) => void;
  onCancel: () => void;
  onComplete: () => void;
}

export function generateCodeLocal(
  wsRef: React.MutableRefObject<WebSocket | null>,
  params: FullGenerationSettings,
  callbacks: CodeGenerationCallbacks
) {
  // Use our simplified WebSocket endpoint
  const wsUrl = `${WS_BACKEND_URL.replace('http', 'ws')}/api/ollama/generate/stream`;
  console.log("Connecting to local Ollama backend @", wsUrl);

  const ws = new WebSocket(wsUrl);
  wsRef.current = ws;

  ws.addEventListener("open", () => {
    // Send simplified request to our Ollama API
    const request = {
      type: "html", // Default to HTML generation
      description: params.prompt || "Create a simple website",
      model_name: params.codeGenerationModel,
      additional_requirements: ""
    };
    
    console.log("Sending request to local backend:", request);
    ws.send(JSON.stringify(request));
  });

  ws.addEventListener("message", (event) => {
    try {
      const response: WebSocketResponse = JSON.parse(event.data);
      console.log("Received from local backend:", response);
      
      switch (response.type) {
        case "status": {
          callbacks.onStatusUpdate(response.message || "", 0);
          break;
        }
        case "complete": {
          const htmlCode = response.data?.html || response.data?.enhanced_code || response.data?.fixed_code || "";
          callbacks.onSetCode(htmlCode, 0);
          callbacks.onVariantComplete(0);
          callbacks.onComplete();
          break;
        }
        case "error": {
          const errorMsg = response.message || ERROR_MESSAGE;
          console.error("Local backend error:", errorMsg);
          callbacks.onVariantError(0, errorMsg);
          toast.error(errorMsg);
          break;
        }
      }
    } catch (error) {
      console.error("Error parsing WebSocket message:", error);
      callbacks.onVariantError(0, "Failed to parse response from local backend");
    }
  });

  ws.addEventListener("close", (event) => {
    console.log("WebSocket connection closed:", event.code, event.reason);
    if (event.code === 1000) {
      // Normal closure
      console.log("WebSocket closed normally");
    } else if (event.code !== 1006) {
      // Not a normal closure, show error
      toast.error("Connection to local backend lost");
    }
  });

  ws.addEventListener("error", (error) => {
    console.error("WebSocket error:", error);
  toast.error("Failed to connect to local backend. Make sure it's running on http://localhost:8000");
    callbacks.onVariantError(0, "WebSocket connection failed");
  });
}

// Also create HTTP-based methods for direct API calls
export async function generateHTMLLocal(
  description: string, 
  model: string = "llama3.2:3b",
  requirements: string = ""
): Promise<string> {
  try {
    const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/generate/html`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        description,
        additional_requirements: requirements,
        model_name: model
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    if (data.success) {
      return data.data.html;
    } else {
      throw new Error(data.error || "Unknown error");
    }
  } catch (error) {
    console.error("Error calling local HTML API:", error);
    toast.error("Failed to generate HTML. Make sure local backend is running.");
    throw error;
  }
}

export async function generateCSSLocal(
  description: string, 
  existingHTML: string = "",
  model: string = "llama3.2:3b"
): Promise<string> {
  try {
    const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/generate/css`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mockup_description: description,
        existing_html: existingHTML,
        model_name: model
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    if (data.success) {
      return data.data.css;
    } else {
      throw new Error(data.error || "Unknown error");
    }
  } catch (error) {
    console.error("Error calling local CSS API:", error);
    toast.error("Failed to generate CSS. Make sure local backend is running.");
    throw error;
  }
}

export async function generateReactLocal(
  description: string, 
  props: string[] = [],
  model: string = "llama3.2:3b"
): Promise<string> {
  try {
    const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/generate/react`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        component_description: description,
        props,
        model_name: model
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    if (data.success) {
      return data.data.react;
    } else {
      throw new Error(data.error || "Unknown error");
    }
  } catch (error) {
    console.error("Error calling local React API:", error);
    toast.error("Failed to generate React component. Make sure local backend is running.");
    throw error;
  }
}

// Health check function
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${HTTP_BACKEND_URL}/api/ollama/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log("Backend health check:", data);
      return data.success;
    }
    return false;
  } catch (error) {
    console.error("Backend health check failed:", error);
    return false;
  }
}
