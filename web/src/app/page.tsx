// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { Heart, Code, Users } from "lucide-react";
import { useMemo } from "react";

import { SiteHeader } from "./chat/components/site-header";
import { Jumbotron } from "./landing/components/jumbotron";
import { Ray } from "./landing/components/ray";
import { CaseStudySection } from "./landing/sections/case-study-section";
import { CoreFeatureSection } from "./landing/sections/core-features-section";
import { JoinCommunitySection } from "./landing/sections/join-community-section";
import { MultiAgentSection } from "./landing/sections/multi-agent-section";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center min-h-screen">
      <SiteHeader />
      <main className="container flex flex-col items-center justify-center gap-32 w-full">
        <Jumbotron />
        
        {/* Enhanced sections with animations */}
        <div className="w-full space-y-32">
          <div className="animate-slide-up">
            <CaseStudySection />
          </div>
          
          <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <MultiAgentSection />
          </div>
          
          <div className="animate-slide-up" style={{ animationDelay: '0.4s' }}>
            <CoreFeatureSection />
          </div>
          
          <div className="animate-slide-up" style={{ animationDelay: '0.6s' }}>
            <JoinCommunitySection />
          </div>
        </div>
      </main>
      
      <Footer />
      <Ray />
    </div>
  );
}

function Footer() {
  const year = useMemo(() => new Date().getFullYear(), []);
  
  return (
    <footer className="w-full mt-24 glass-effect border-t border-white/10 dark:border-white/5">
      <div className="container flex flex-col items-center justify-center py-16 space-y-8">
        {/* Enhanced quote section */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-12 h-px bg-gradient-to-r from-transparent via-border to-transparent"></div>
          </div>
          <p className="text-center font-serif text-xl md:text-2xl gradient-text font-medium max-w-2xl">
            &quot;Originated from Open Source, give back to Open Source.&quot;
          </p>
          <div className="flex justify-center">
            <div className="w-12 h-px bg-gradient-to-r from-transparent via-border to-transparent"></div>
          </div>
        </div>

        {/* Enhanced links section */}
        <div className="flex flex-wrap justify-center gap-8 text-sm text-muted-foreground">
          <a 
            href="https://github.com/bytedance/deer-flow" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-foreground transition-colors duration-300 hover-lift"
          >
            <Code className="w-4 h-4" />
            <span>Source Code</span>
          </a>
          <a 
            href="https://github.com/bytedance/deer-flow/issues" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-foreground transition-colors duration-300 hover-lift"
          >
            <Users className="w-4 h-4" />
            <span>Community</span>
          </a>
          <a 
            href="https://github.com/bytedance/deer-flow/blob/main/LICENSE" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-foreground transition-colors duration-300 hover-lift"
          >
            <Heart className="w-4 h-4" />
            <span>MIT License</span>
          </a>
        </div>

        {/* Copyright */}
        <div className="text-center text-xs text-muted-foreground space-y-1">
          <p>&copy; {year} DeerFlow. All rights reserved.</p>
          <p className="flex items-center justify-center gap-1">
            Made with <Heart className="w-3 h-3 text-red-500 animate-pulse" /> by the DeerFlow Team
          </p>
        </div>
      </div>
    </footer>
  );
}
