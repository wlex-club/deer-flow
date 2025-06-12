"use client";

// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import React, { useEffect } from "react";
import { cn } from "~/lib/utils";

interface TextReadabilityEnhancerProps {
  children: React.ReactNode;
  className?: string;
  enhanced?: boolean;
  highContrast?: boolean;
}

export function TextReadabilityEnhancer({
  children,
  className,
  enhanced = true,
  highContrast = false,
}: TextReadabilityEnhancerProps) {
  useEffect(() => {
    // Enhanced text readability fixes
    const style = document.createElement("style");
    style.textContent = `
      /* Global text readability fixes */
      * {
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
      }
      
      /* Fix low opacity text elements */
      .opacity-60, .opacity-70, .opacity-80 {
        opacity: 1 !important;
      }
      
      .opacity-50 {
        opacity: 0.8 !important;
      }
      
      .opacity-40 {
        opacity: 0.7 !important;
      }
      
      .opacity-30 {
        opacity: 0.6 !important;
      }
      
      /* Ensure all interactive elements have proper contrast */
      button, [role="button"], a, input, textarea, select {
        color: var(--foreground) !important;
      }
      
      button:disabled, [role="button"]:disabled {
        opacity: 0.5 !important;
        color: var(--muted-foreground) !important;
      }
      
      /* Force readable text for common classes */
      .text-muted-foreground {
        color: var(--muted-foreground) !important;
        opacity: 1 !important;
      }
      
      /* Fix any remaining transparent text */
      [style*="opacity: 0.6"], [style*="opacity: 0.7"], [style*="opacity: 0.8"] {
        opacity: 1 !important;
      }
      
      /* Enhance contrast for better readability */
      .message-content, .prose, .prose * {
        color: var(--foreground) !important;
      }
      
      /* Chat specific fixes */
      .user-message, .user-message * {
        color: white !important;
      }
      
      .assistant-message, .assistant-message * {
        color: var(--foreground) !important;
      }
      
      /* Input and form fixes */
      .input-box-content, .input-box-content * {
        color: var(--foreground) !important;
      }
      
      /* Tooltip and dropdown fixes */
      [role="tooltip"], [role="menu"], [role="listbox"] {
        color: var(--foreground) !important;
        background: var(--popover) !important;
      }
      
      /* Card and content fixes */
      .card-content, .card-description, .card-header {
        color: var(--foreground) !important;
      }
      
      /* Settings page fixes */
      .settings-content, .settings-content * {
        color: var(--foreground) !important;
      }
      
      .settings-disabled {
        color: var(--muted-foreground) !important;
        opacity: 1 !important;
      }
    `;
    
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div
      className={cn(
        // Base readability improvements
        enhanced && "text-readable",
        highContrast && "high-contrast",
        className
      )}
      style={{
        // Ensure text is always readable
        WebkitFontSmoothing: "antialiased",
        MozOsxFontSmoothing: "grayscale",
        textRendering: "optimizeLegibility",
        // Force minimum contrast
        filter: highContrast ? "contrast(1.3) brightness(1.1)" : undefined,
      }}
    >
      {children}
    </div>
  );
} 