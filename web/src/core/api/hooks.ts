"use client";

// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { useEffect, useRef, useState } from "react";

import { env } from "~/env";

import { useReplay } from "../replay";

import { fetchReplayTitle } from "./chat";
import { getRAGConfig } from "./rag";
import { checkServerStatus, logServerDiagnostics } from "./server-status";

export function useReplayMetadata() {
  const { isReplay } = useReplay();
  const [title, setTitle] = useState<string | null>(null);
  const isLoading = useRef(false);
  const [error, setError] = useState<boolean>(false);
  useEffect(() => {
    if (!isReplay) {
      return;
    }
    if (title || isLoading.current) {
      return;
    }
    isLoading.current = true;
    fetchReplayTitle()
      .then((title) => {
        setError(false);
        setTitle(title ?? null);
        if (title) {
          document.title = `${title} - DeerFlow`;
        }
      })
      .catch(() => {
        setError(true);
        setTitle("Error: the replay is not available.");
        document.title = "DeerFlow";
      })
      .finally(() => {
        isLoading.current = false;
      });
  }, [isLoading, isReplay, title]);
  return { title, isLoading, hasError: error };
}

export function useRAGProvider() {
  const [loading, setLoading] = useState(true);
  const [provider, setProvider] = useState<string | null>(null);
  const [serverStatus, setServerStatus] = useState<"checking" | "online" | "offline">("checking");

  useEffect(() => {
    if (env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY) {
      setLoading(false);
      setServerStatus("offline");
      return;
    }

    // First check server status
    checkServerStatus()
      .then((status) => {
        logServerDiagnostics(status);
        setServerStatus(status.isRunning ? "online" : "offline");
        
        if (status.isRunning) {
          // If server is running, get RAG config
          return getRAGConfig();
        } else {
          throw new Error(`Server is not running: ${status.error}`);
        }
      })
      .then(setProvider)
      .catch((e) => {
        setProvider(null);
        setServerStatus("offline");
        console.error("Failed to get RAG provider", e);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { provider, loading, serverStatus };
}
