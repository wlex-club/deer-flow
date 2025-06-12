// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { resolveServiceURL } from "./resolve-service-url";

export interface ServerStatus {
  isRunning: boolean;
  url: string;
  error?: string;
  responseTime?: number;
}

export async function checkServerStatus(): Promise<ServerStatus> {
  const url = resolveServiceURL("rag/config");
  const startTime = Date.now();
  
  try {
    console.log("🔍 Checking server status at:", url);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
    
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    const responseTime = Date.now() - startTime;
    
    if (response.ok) {
      console.log("✅ Server is running and responsive");
      return {
        isRunning: true,
        url,
        responseTime,
      };
    } else {
      console.log("⚠️ Server responded with error:", response.status);
      return {
        isRunning: false,
        url,
        responseTime,
        error: `HTTP ${response.status}: ${response.statusText}`,
      };
    }
  } catch (error) {
    const responseTime = Date.now() - startTime;
    console.error("❌ Server is not accessible:", error);
    
    let errorMessage = "Unknown error";
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        errorMessage = "Request timeout (server not responding)";
      } else if (error.message.includes("Failed to fetch")) {
        errorMessage = "Connection refused (server not running)";
      } else {
        errorMessage = error.message;
      }
    }
    
    return {
      isRunning: false,
      url,
      responseTime,
      error: errorMessage,
    };
  }
}

export function logServerDiagnostics(status: ServerStatus) {
  console.log("🔧 ===== SERVER DIAGNOSTICS =====");
  console.log("📍 Target URL:", status.url);
  console.log("🏃 Server Running:", status.isRunning ? "✅ YES" : "❌ NO");
  console.log("⏱️ Response Time:", status.responseTime + "ms");
  
  if (status.error) {
    console.log("❌ Error:", status.error);
  }
  
  if (!status.isRunning) {
    console.log("🔧 ===== TROUBLESHOOTING STEPS =====");
    console.log("1. 🐍 Make sure Python backend is running:");
    console.log("   cd E:\\office-project\\deer-flow");
    console.log("   .venv\\Scripts\\Activate.ps1");
    console.log("   python server.py --reload");
    console.log("");
    console.log("2. 🌐 Verify the server starts on port 8000:");
    console.log("   Look for: 'Uvicorn running on http://localhost:8000'");
    console.log("");
    console.log("3. 🔍 Test manually in browser:");
    console.log("   Visit: http://localhost:8000/api/rag/config");
    console.log("");
    console.log("4. 🚪 Check if port 8000 is available:");
    console.log("   netstat -ano | findstr :8000");
    console.log("🔧 ===============================");
  }
} 