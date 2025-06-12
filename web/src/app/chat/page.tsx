// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

"use client";

import { GithubOutlined } from "@ant-design/icons";
import { Sparkles, Settings } from "lucide-react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { Suspense } from "react";

import { Button } from "~/components/ui/button";

import { Logo } from "../../components/deer-flow/logo";
import { ThemeToggle } from "../../components/deer-flow/theme-toggle";
import { Tooltip } from "../../components/deer-flow/tooltip";
import { SettingsDialog } from "../settings/dialogs/settings-dialog";

const Main = dynamic(() => import("./main"), {
  ssr: false,
  loading: () => (
    <div className="flex h-full w-full items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="relative">
          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 animate-pulse"></div>
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 animate-ping opacity-20"></div>
        </div>
        <p className="text-muted-foreground animate-pulse">Loading DeerFlow...</p>
      </div>
    </div>
  ),
});

export default function HomePage() {
  return (
    <div className="flex h-screen w-screen justify-center overscroll-none bg-gradient-to-br from-background via-background to-muted/20">
      <header className="fixed top-0 left-0 flex h-14 w-full items-center justify-between px-4 glass-effect z-50 border-b border-white/10 dark:border-white/5">
        <div className="flex items-center gap-4">
          <Logo />
          <div className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-green-500/10 rounded-full border border-green-500/20">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs font-medium text-green-600 dark:text-green-400">Online</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <Tooltip title="Star DeerFlow on GitHub">
            <Button variant="ghost" size="icon" asChild className="hover-lift">
              <Link
                href="https://github.com/bytedance/deer-flow"
                target="_blank"
                className="flex items-center justify-center"
              >
                <GithubOutlined className="transition-transform duration-300 hover:scale-110" />
              </Link>
            </Button>
          </Tooltip>
          
          <ThemeToggle />
          
          <Suspense fallback={
            <Button variant="ghost" size="icon" disabled>
              <Settings className="w-4 h-4" />
            </Button>
          }>
            <SettingsDialog />
          </Suspense>
        </div>
      </header>
      
      <div className="flex-1 pt-14 relative overflow-hidden">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(120,119,198,0.1),transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(120,119,198,0.05),transparent_50%)]"></div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_80%,rgba(255,119,198,0.05),transparent_50%)]"></div>
        </div>
        
        <Main />
      </div>
    </div>
  );
}
