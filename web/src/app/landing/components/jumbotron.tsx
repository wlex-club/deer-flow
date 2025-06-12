// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { GithubFilled } from "@ant-design/icons";
import { ChevronRight, Sparkles, Zap } from "lucide-react";
import Link from "next/link";

import { AuroraText } from "~/components/magicui/aurora-text";
import { FlickeringGrid } from "~/components/magicui/flickering-grid";
import { FloatingParticles } from "~/components/magicui/floating-particles";
import { GradientOrb } from "~/components/magicui/gradient-orb";
import { Button } from "~/components/ui/button";
import { env } from "~/env";

export function Jumbotron() {
  return (
    <section className="relative flex h-[95vh] w-full flex-col items-center justify-center pb-15 overflow-hidden">
      {/* Enhanced background layers */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/20 via-purple-50/20 to-pink-50/20 dark:from-blue-950/20 dark:via-purple-950/20 dark:to-pink-950/20" />
      
      {/* Gradient orbs for depth */}
      <GradientOrb size="xl" color="blue" className="top-0 left-0 -translate-x-1/2 -translate-y-1/2" />
      <GradientOrb size="lg" color="purple" className="top-1/4 right-0 translate-x-1/2" />
      <GradientOrb size="md" color="pink" className="bottom-1/4 left-1/4" />
      
      {/* Floating particles */}
      <FloatingParticles count={30} />
      
      <FlickeringGrid
        id="deer-hero-bg"
        className={`absolute inset-0 z-0 [mask-image:radial-gradient(1000px_circle_at_center,white,transparent)]`}
        squareSize={4}
        gridGap={4}
        color="#60A5FA"
        maxOpacity={0.2}
        flickerChance={0.15}
      />
      
      {/* Enhanced floating decoration elements */}
      <div className="absolute top-20 left-20 w-3 h-3 bg-blue-400 rounded-full opacity-60 animate-float shadow-lg shadow-blue-400/30" style={{ animationDelay: '0s' }} />
      <div className="absolute top-32 right-32 w-2 h-2 bg-purple-400 rounded-full opacity-60 animate-float shadow-lg shadow-purple-400/30" style={{ animationDelay: '2s' }} />
      <div className="absolute bottom-40 left-32 w-4 h-4 bg-pink-400 rounded-full opacity-60 animate-float shadow-lg shadow-pink-400/30" style={{ animationDelay: '4s' }} />
      <div className="absolute bottom-60 right-20 w-2 h-2 bg-indigo-400 rounded-full opacity-60 animate-float shadow-lg shadow-indigo-400/30" style={{ animationDelay: '1s' }} />
      
      <FlickeringGrid
        id="deer-hero"
        className="absolute inset-0 z-0 translate-y-[2vh] mask-[url(/images/deer-hero.svg)] mask-size-[100vw] mask-center mask-no-repeat md:mask-size-[72vh]"
        squareSize={3}
        gridGap={6}
        color="#60A5FA"
        maxOpacity={0.7}
        flickerChance={0.18}
      />
      
      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-center gap-12 animate-slide-up">
        {/* Enhanced title with icons */}
        <div className="flex flex-col items-center gap-6">
          <div className="flex items-center gap-3 text-sm font-medium text-muted-foreground mb-2">
            <Sparkles className="w-4 h-4 text-blue-500 animate-pulse" />
            <span className="px-4 py-2 bg-white/10 dark:bg-black/20 backdrop-blur-sm rounded-full border border-white/20 dark:border-white/10 shadow-lg">
              AI-Powered Research Platform
            </span>
            <Zap className="w-4 h-4 text-purple-500 animate-pulse" />
          </div>
          
          <h1 className="text-center text-4xl font-bold md:text-7xl leading-tight">
            <span className="gradient-text block mb-2 drop-shadow-sm">
              Deep Research{" "}
            </span>
            <AuroraText className="text-3xl md:text-6xl drop-shadow-sm">at Your Fingertips</AuroraText>
          </h1>
        </div>

        {/* Enhanced description */}
        <div className="max-w-4xl p-4">
          <p className="text-center text-base md:text-2xl leading-relaxed text-foreground/90">
                          Meet <span className="font-semibold gradient-text-readable">DeerFlow</span>, your personal Deep Research assistant. 
            With powerful tools like search engines, web crawlers, Python and MCP services, 
            it delivers <span className="text-blue-600 dark:text-blue-400 font-medium">instant insights</span>, 
            <span className="text-purple-600 dark:text-purple-400 font-medium"> comprehensive reports</span>, 
            and even <span className="text-pink-600 dark:text-pink-400 font-medium">captivating podcasts</span>.
          </p>
        </div>

        {/* Enhanced buttons */}
        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6">
          <Button 
            className="btn-gradient text-white font-semibold text-lg h-12 px-8 shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 border-0" 
            size="lg" 
            asChild
          >
            <Link
              target={env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY ? "_blank" : undefined}
              href={
                env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY
                  ? "https://github.com/bytedance/deer-flow"
                  : "/chat"
              }
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Get Started 
              <ChevronRight className="w-5 h-5 ml-2" />
            </Link>
          </Button>
          
          {!env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY && (
            <Button
              className="glass-effect hover-lift text-lg h-12 px-8 font-medium border-2 border-white/30 dark:border-white/20 backdrop-blur-sm transition-all duration-300 shadow-xl"
              size="lg"
              variant="outline"
              asChild
            >
              <Link
                href="https://github.com/bytedance/deer-flow"
                target="_blank"
              >
                <GithubFilled className="mr-2" />
                Learn More
              </Link>
            </Button>
          )}
        </div>

        {/* Enhanced feature highlights */}
        <div className="flex flex-wrap justify-center gap-6 mt-8 text-sm text-muted-foreground">
          <div className="flex items-center gap-2 px-3 py-2 bg-white/5 dark:bg-black/10 rounded-full backdrop-blur-sm">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse shadow-sm shadow-green-400/50"></div>
            <span>Multi-Agent Research</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 bg-white/5 dark:bg-black/10 rounded-full backdrop-blur-sm">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse shadow-sm shadow-blue-400/50"></div>
            <span>Real-time Analysis</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 bg-white/5 dark:bg-black/10 rounded-full backdrop-blur-sm">
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse shadow-sm shadow-purple-400/50"></div>
            <span>Content Generation</span>
          </div>
        </div>
      </div>
      
      {/* Enhanced footer note */}
      <div className="absolute bottom-8 flex items-center gap-2 text-xs text-muted-foreground backdrop-blur-sm bg-white/10 dark:bg-black/20 px-4 py-2 rounded-full">
        <Sparkles className="w-3 h-3 animate-pulse" />
        <p>DEER stands for Deep Exploration and Efficient Research</p>
        <Sparkles className="w-3 h-3 animate-pulse" />
      </div>
    </section>
  );
}
