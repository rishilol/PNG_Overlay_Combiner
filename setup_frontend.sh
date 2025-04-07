#!/bin/bash

# Create React app in the frontend directory
npx create-react-app frontend

# Navigate to frontend directory
cd frontend

# Install additional dependencies
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material axios

# Remove unnecessary files
rm src/App.test.js src/logo.svg src/reportWebVitals.js src/setupTests.js

# Create necessary directories
mkdir -p src/components

# Return to root directory
cd .. 