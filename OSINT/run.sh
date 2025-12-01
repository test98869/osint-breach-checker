#!/bin/bash

echo "🚀 Starting OSINT Breach Checker Web UI..."
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Starting server..."
echo "🌐 Open your browser to: http://localhost:5000"
echo ""

python app.py
