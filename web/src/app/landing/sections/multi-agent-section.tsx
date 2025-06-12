// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { Brain, Network, Zap } from "lucide-react";

import { FloatingParticles } from "~/components/magicui/floating-particles";
import { GradientOrb } from "~/components/magicui/gradient-orb";

import { MultiAgentVisualization } from "../components/multi-agent-visualization";
import { SectionHeader } from "../components/section-header";

export function MultiAgentSection() {
  return (
    <section className="relative flex w-full flex-col items-center justify-center py-20">
      {/* Enhanced background with tech vibes */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-purple-500/5 to-blue-500/5 rounded-3xl"></div>
      
      {/* Background decorations */}
      <GradientOrb size="xl" color="purple" className="top-0 right-0 translate-x-1/3 -translate-y-1/3 opacity-40" />
      <GradientOrb size="lg" color="blue" className="bottom-0 left-0 -translate-x-1/3 translate-y-1/3 opacity-40" />
      
      {/* Tech-themed floating particles */}
      <FloatingParticles count={25} className="opacity-50" />
      
      {/* Grid pattern overlay */}
      <div className="absolute inset-0 opacity-5">
        <div 
          className="w-full h-full"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3e%3cdefs%3e%3cpattern id='grid' width='60' height='60' patternUnits='userSpaceOnUse'%3e%3cpath d='m 60 0 l 0 60 l -60 0 l 0 -60 z' fill='none' stroke='%23666' stroke-width='1'/%3e%3c/pattern%3e%3c/defs%3e%3crect width='100%25' height='100%25' fill='url(%23grid)' /%3e%3c/svg%3e")`,
          }}
        />
      </div>
      
      <div className="relative z-10 w-full">
        <SectionHeader
          anchor="multi-agent-architecture"
          title="Multi-Agent Architecture"
          description="Experience the powerful collaboration of specialized AI agents working together seamlessly"
        />
        
        {/* Enhanced feature highlights above visualization */}
        <div className="flex flex-wrap justify-center gap-8 mb-12 px-4">
          <div className="flex items-center gap-3 px-4 py-3 bg-white/5 dark:bg-black/10 backdrop-blur-sm rounded-full border border-white/10 hover-lift">
            <div className="p-2 bg-purple-500/20 rounded-full">
              <Brain className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h4 className="text-sm font-medium">Intelligent Coordination</h4>
              <p className="text-xs text-muted-foreground">Smart task delegation</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3 px-4 py-3 bg-white/5 dark:bg-black/10 backdrop-blur-sm rounded-full border border-white/10 hover-lift">
            <div className="p-2 bg-blue-500/20 rounded-full">
              <Network className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h4 className="text-sm font-medium">Collaborative Network</h4>
              <p className="text-xs text-muted-foreground">Seamless handoffs</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3 px-4 py-3 bg-white/5 dark:bg-black/10 backdrop-blur-sm rounded-full border border-white/10 hover-lift">
            <div className="p-2 bg-green-500/20 rounded-full">
              <Zap className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <h4 className="text-sm font-medium">Real-time Processing</h4>
              <p className="text-xs text-muted-foreground">Instant results</p>
            </div>
          </div>
        </div>
        
        {/* Enhanced visualization container */}
        <div className="flex h-[70vh] w-full flex-col items-center justify-center animate-slide-up">
          <div className="h-full w-full relative">
            {/* Glow effect around visualization */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/10 to-transparent blur-xl opacity-50 animate-pulse"></div>
            
            {/* Main visualization */}
            <div className="relative z-10 h-full w-full glass-effect border border-white/20 dark:border-white/10 rounded-2xl overflow-hidden">
              <MultiAgentVisualization />
            </div>
            
            {/* Corner decorations */}
            <div className="absolute top-4 left-4 w-3 h-3 bg-purple-400 rounded-full animate-pulse opacity-60"></div>
            <div className="absolute top-4 right-4 w-2 h-2 bg-blue-400 rounded-full animate-float opacity-60" style={{ animationDelay: '1s' }}></div>
            <div className="absolute bottom-4 left-4 w-2 h-2 bg-green-400 rounded-full animate-pulse opacity-60" style={{ animationDelay: '2s' }}></div>
            <div className="absolute bottom-4 right-4 w-3 h-3 bg-pink-400 rounded-full animate-float opacity-60" style={{ animationDelay: '0.5s' }}></div>
          </div>
        </div>
        
        {/* Bottom info section */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-full border border-white/10 backdrop-blur-sm">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-muted-foreground">Live Architecture Visualization</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
