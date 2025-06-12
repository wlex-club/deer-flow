// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { StarFilledIcon, GitHubLogoIcon } from "@radix-ui/react-icons";
import { Sparkles } from "lucide-react";
import Link from "next/link";

import { NumberTicker } from "~/components/magicui/number-ticker";
import { Button } from "~/components/ui/button";
import { env } from "~/env";

export async function SiteHeader() {
  return (
    <header className="glass-effect sticky top-0 left-0 z-40 flex h-16 w-full flex-col items-center transition-all duration-300">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-3 text-xl font-bold">
          <div className="relative">
            <span className="text-3xl animate-float">🦌</span>
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-blue-400 rounded-full animate-ping opacity-75"></div>
          </div>
          <span className="gradient-text">DeerFlow</span>
          <div className="hidden sm:flex items-center gap-2 ml-3 px-2 py-1 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-full border border-white/20 dark:border-white/10">
            <Sparkles className="w-3 h-3 text-blue-500" />
            <span className="text-xs font-medium text-muted-foreground">Research AI</span>
          </div>
        </div>
        
        <div className="relative flex items-center">
          {/* Enhanced glow effect */}
          <div
            className="pointer-events-none absolute inset-0 z-0 h-full w-full rounded-full opacity-50 blur-2xl transition-opacity duration-500 hover:opacity-80"
            style={{
              background: "linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
              filter: "blur(20px)",
            }}
          />
          
          <Button
            variant="outline"
            size="sm"
            asChild
            className="group relative z-10 glass-effect hover-lift border-2 border-white/30 dark:border-white/20 font-semibold transition-all duration-300 hover:border-white/50 dark:hover:border-white/30"
          >
            <Link href="https://github.com/bytedance/deer-flow" target="_blank">
              <GitHubLogoIcon className="size-4 mr-2 transition-transform duration-300 group-hover:scale-110" />
              <span className="hidden sm:inline">Star on</span> GitHub
              {env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY &&
                env.GITHUB_OAUTH_TOKEN && <StarCounter />}
            </Link>
          </Button>
        </div>
      </div>
      
      {/* Enhanced divider */}
      <div className="w-full h-px bg-gradient-to-r from-transparent via-border/50 to-transparent opacity-60" />
    </header>
  );
}

export async function StarCounter() {
  let stars = 1000; // Default value

  try {
    const response = await fetch(
      "https://api.github.com/repos/bytedance/deer-flow",
      {
        headers: env.GITHUB_OAUTH_TOKEN
          ? {
              Authorization: `Bearer ${env.GITHUB_OAUTH_TOKEN}`,
              "Content-Type": "application/json",
            }
          : {},
        next: {
          revalidate: 3600,
        },
      },
    );

    if (response.ok) {
      const data = await response.json();
      stars = data.stargazers_count ?? stars; // Update stars if API response is valid
    }
  } catch (error) {
    console.error("Error fetching GitHub stars:", error);
  }
  
  return (
    <div className="flex items-center gap-1 ml-2 pl-2 border-l border-white/20 dark:border-white/10">
      <StarFilledIcon className="size-3 text-yellow-500 transition-all duration-300 group-hover:text-yellow-400 group-hover:drop-shadow-sm" />
      {stars && (
        <NumberTicker 
          className="font-mono text-xs font-bold tabular-nums" 
          value={stars} 
        />
      )}
    </div>
  );
}
