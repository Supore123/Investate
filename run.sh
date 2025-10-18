#!/bin/bash

# Update property data
echo "🏠 Fetching property data..."
python3 property_fetcher.py

# Start the web server
echo "🚀 Starting local server at http://localhost:8000 ..."
python3 -m http.server 8000
