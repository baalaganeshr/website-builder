# Local AI Website Builder

This project is a simple, local-first AI website builder that uses Ollama to generate websites from a text description.

## Features

-   **Backend:** FastAPI server that connects to a local Ollama instance.
-   **Frontend:** Simple React/Vite application to interact with the backend.
-   **Local First:** All processing is done locally via Ollama. No external APIs are needed.

## Prerequisites

-   [Node.js](https://nodejs.org/) (v18 or higher)
-   [Python](https://www.python.org/) (v3.10 or higher)
-   [Poetry](https://python-poetry.org/) for Python dependency management.
-   [Ollama](https://ollama.ai/) installed and running.

## Setup

1.  **Install Ollama Models:**
    Pull the required models that you want to use. The application is tested with the following models:
    ```bash
    ollama pull gpt-oss-20b
    ollama pull llama3.2:3b
    ```

2.  **Install Backend Dependencies:**
    Navigate to the `backend` directory and install the dependencies using Poetry.
    ```bash
    cd backend
    poetry install
    cd ..
    ```

3.  **Install Frontend Dependencies:**
    Navigate to the `frontend` directory and install the dependencies using npm (or your preferred package manager).
    ```bash
    cd frontend
    npm install
    cd ..
    ```

## Running the Application

1.  **Start the Backend Server:**
    From the `backend` directory, run the FastAPI server using uvicorn.
    ```bash
    cd backend
    poetry run uvicorn main:app --reload --port 8000
    ```
    The backend will be available at `http://localhost:8000`.

2.  **Start the Frontend Application:**
    In a new terminal, navigate to the `frontend` directory and start the Vite development server.
    ```bash
    cd frontend
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## How to Use

1.  Open your browser and navigate to `http://localhost:5173`.
2.  In the textarea, describe the website you want to create.
3.  Select the Ollama model you want to use from the dropdown.
4.  Click the "Generate Website" button.
5.  The generated website will be displayed in the preview pane on the right.
