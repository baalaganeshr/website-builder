#!/bin/bash

echo "🚀 Setting up Website Builder with AI Screenshot-to-Code..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    pip install --upgrade poetry
fi

# Setup backend
echo "🔧 Setting up backend..."
cd backend
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "Please add your API keys to backend/.env"
fi

poetry install
cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend
yarn install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🔑 Next steps:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Optionally add your Anthropic API key to backend/.env"
echo "3. Run the development servers:"
echo "   - Backend: cd backend && poetry run uvicorn main:app --reload --port 7001"
echo "   - Frontend: cd frontend && yarn dev"
echo "4. Open http://localhost:5173 in your browser"
