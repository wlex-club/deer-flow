"use client";

// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { useRAGProvider } from "~/core/api/hooks";
import { cn } from "~/lib/utils";

export function ServerStatusIndicator() {
  const { serverStatus } = useRAGProvider();

  if (serverStatus === "online") {
    return (
      <div className="fixed bottom-4 right-4 z-50 flex items-center gap-2 rounded-lg bg-green-50 border border-green-200 px-3 py-2 text-sm text-green-700 shadow-sm">
        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
        <span>Backend Connected</span>
      </div>
    );
  }

  if (serverStatus === "offline") {
    return (
      <div className="fixed bottom-4 right-4 z-50 flex items-center gap-2 rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-700 shadow-sm">
        <div className="h-2 w-2 rounded-full bg-red-500" />
        <span>Backend Offline</span>
        <button
          onClick={() => {
            console.log("🔧 Manual server check requested");
            window.location.reload();
          }}
          className="ml-2 text-xs underline hover:no-underline"
        >
          Retry
        </button>
      </div>
    );
  }

  if (serverStatus === "checking") {
    return (
      <div className="fixed bottom-4 right-4 z-50 flex items-center gap-2 rounded-lg bg-yellow-50 border border-yellow-200 px-3 py-2 text-sm text-yellow-700 shadow-sm">
        <div className="h-2 w-2 rounded-full bg-yellow-500 animate-pulse" />
        <span>Connecting...</span>
      </div>
    );
  }

  return null;
} 