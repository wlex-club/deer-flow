import type { Resource } from "../messages";

import { resolveServiceURL } from "./resolve-service-url";

export function queryRAGResources(query: string) {
  const url = resolveServiceURL(`rag/resources?query=${query}`);
  console.log("🔍 Querying RAG resources from:", url);
  
  return fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      console.log("📡 RAG resources response status:", res.status);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then((res) => {
      console.log("✅ RAG resources received:", res.resources?.length ?? 0, "items");
      return res.resources as Array<Resource>;
    })
    .catch((err) => {
      console.error("❌ Failed to query RAG resources:", err);
      console.error("🔧 Returning empty array as fallback");
      return [];
    });
}

export function getRAGConfig() {
  const url = resolveServiceURL(`rag/config`);
  console.log("🔍 Attempting to fetch RAG config from:", url);
  
  return fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      console.log("📡 RAG config response status:", res.status);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      return res.json();
    })
    .then((res) => {
      console.log("✅ RAG config received:", res);
      return res.provider;
    })
    .catch((err) => {
      console.error("❌ Failed to get RAG config:", err);
      console.error("🔧 Please ensure the backend server is running on port 8000");
      throw err;
    });
}
