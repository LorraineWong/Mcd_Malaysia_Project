// src/apiConfig.js
// Centralized API endpoint configuration for the project.
// Use environment variable, fallback to localhost as default.
export const API_URL = import.meta.env.VITE_API_URL || 'http://0.0.0.0:10000'
