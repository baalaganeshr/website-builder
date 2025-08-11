# Website Builder with AI Screenshot-to-Code

An advanced website builder that combines AI-powered screenshot-to-code functionality with comprehensive web development tools. Convert screenshots, mockups and Figma designs into clean, functional code using AI, and then enhance them with additional website building features. Now supporting Claude Sonnet 3.7, GPT-4o, and **local Ollama models**!

## 🌟 Features

### AI-Powered Code Generation

- **Screenshot to Code**: Convert any screenshot, mockup, or Figma design into functional code
- **Multiple Output Formats**: HTML + Tailwind, HTML + CSS, React + Tailwind, Vue + Tailwind, Bootstrap, Ionic + Tailwind, SVG
- **Advanced AI Models**: Support for Claude Sonnet 3.7, GPT-4o, and **local Ollama models** (including your GPT-20B)
- **Local AI Support**: Use Ollama for privacy-focused, offline code generation
- **Video to Code**: Experimental support for screen recordings

### Website Building Tools

- **Live Preview**: Real-time preview of generated code
- **Code Editor**: Built-in code editor with syntax highlighting
- **Component Library**: Reusable UI components
- **Responsive Design**: Mobile-first responsive layouts
- **Export Options**: Download complete projects or individual files

### Development Features

- **Hot Reload**: Instant updates during development
- **Modern Stack**: React + TypeScript + Vite + Tailwind CSS
- **FastAPI Backend**: High-performance Python backend
- **WebSocket Support**: Real-time communication between frontend and backend

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- API Keys: OpenAI (required) and/or Anthropic (optional)

### Automated Setup

#### Windows (PowerShell)

```powershell
./setup.ps1
```

#### Linux/macOS (Bash)

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd website-builder
```

2. **Backend Setup**

```bash
cd backend
pip install --upgrade poetry
poetry install
cp .env.example .env
# Add your API keys to .env
```

3. **Frontend Setup**

```bash
cd frontend
yarn install
# or npm install
```

4. **Environment Configuration**

Add your API keys to `backend/.env`:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # Optional

# For Ollama local models (your GPT-20B)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gpt-20b
```

## 🏃‍♂️ Running the Application

### For Cloud AI Models (OpenAI/Anthropic)

### Start Backend

```bash
cd backend
poetry run uvicorn main:app --reload --port 7001
```

### Start Frontend

```bash
cd frontend
yarn dev
# or npm run dev
```

### For Local AI Models (Ollama)

1. **Start Ollama** (make sure your GPT-20B model is available):

```bash
ollama serve
# Verify your model is available:
ollama list
```

2. **Start the Backend**:

```bash
cd backend
poetry run uvicorn main:app --reload --port 7001
```

3. **Start the Frontend**:

```bash
cd frontend
yarn dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🐳 Docker Setup

For a quick setup using Docker:

```bash
echo "OPENAI_API_KEY=sk-your-key" > .env
echo "ANTHROPIC_API_KEY=your-key" >> .env
docker-compose up -d --build
```

The app will be available at [http://localhost:5173](http://localhost:5173).

## 🎯 Usage

1. **Upload Screenshot**: Drag and drop or select a screenshot/mockup
2. **Choose Output Format**: Select your preferred framework (React, Vue, HTML, etc.)
3. **Select AI Model**: Choose between:
   - **Cloud Models**: Claude Sonnet 3.7, GPT-4o (requires API keys)
   - **Local Models**: Your GPT-20B via Ollama (private, offline)
4. **Generate Code**: Click generate and watch AI create your code
5. **Edit & Enhance**: Use the built-in editor to refine the generated code
6. **Export**: Download your project or copy the code

## 🔧 Configuration

### Backend Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (optional for cloud models)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional for cloud models)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL_NAME`: Your local model name (e.g., gpt-20b)
- `OPENAI_BASE_URL`: Custom OpenAI API base URL (optional, for proxies)
- `PORT`: Backend server port (default: 7001)

### Frontend Environment Variables

- `VITE_HTTP_BACKEND_URL`: Backend HTTP URL (default: http://localhost:7001)
- `VITE_WS_BACKEND_URL`: Backend WebSocket URL (default: ws://localhost:7001)

## 🧪 Testing

### Backend Tests
```bash
cd backend
poetry run pytest
```

### Frontend Tests
```bash
cd frontend
yarn test
# or npm test
```

### Run All Tests
```bash
npm run test
```

**NYTimes**

| Original                                                                                                                                                        | Replica                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="1238" alt="Screenshot 2023-11-20 at 12 54 03 PM" src="https://github.com/abi/screenshot-to-code/assets/23818/3b644dfa-9ca6-4148-84a7-3405b6671922"> | <img width="1414" alt="Screenshot 2023-11-20 at 12 59 56 PM" src="https://github.com/abi/screenshot-to-code/assets/23818/26201c9f-1a28-4f35-a3b1-1f04e2b8ce2a"> |

**Instagram page (with not Taylor Swift pics)**

https://github.com/abi/screenshot-to-code/assets/23818/503eb86a-356e-4dfc-926a-dabdb1ac7ba1

**Hacker News** but it gets the colors wrong at first so we nudge it

https://github.com/abi/screenshot-to-code/assets/23818/3fec0f77-44e8-4fb3-a769-ac7410315e5d
