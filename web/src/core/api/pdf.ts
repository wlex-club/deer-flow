// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { resolveServiceURL } from "./resolve-service-url";

export async function generatePDF(content: string, title = "Report") {
  const response = await fetch(resolveServiceURL("pdf/generate"), {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content, title }),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const arrayBuffer = await response.arrayBuffer();
  const blob = new Blob([arrayBuffer], { 
    type: "application/pdf" 
  });
  const pdfUrl = URL.createObjectURL(blob);
  return pdfUrl;
} 