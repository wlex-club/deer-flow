// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { Bird, Microscope, Podcast, Usb, User, Sparkles, Zap, Brain, Cpu } from "lucide-react";

import { BentoCard, BentoGrid } from "~/components/magicui/bento-grid";

import { SectionHeader } from "../components/section-header";

const features = [
  {
    Icon: Microscope,
    name: "Dive Deeper and Reach Wider",
    description:
      "Unlock deeper insights with advanced tools. Our powerful search + crawling and Python tools gathers comprehensive data, delivering in-depth reports to enhance your study.",
    href: "https://github.com/bytedance/deer-flow/blob/main/src/tools",
    cta: "Learn more",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-purple-500/10 to-transparent opacity-60">
        <div className="absolute top-4 right-4 w-8 h-8 bg-blue-400/30 rounded-full animate-pulse"></div>
        <div className="absolute bottom-8 left-8 w-6 h-6 bg-purple-400/30 rounded-full animate-float"></div>
        <Sparkles className="absolute top-8 left-6 w-5 h-5 text-blue-400/50" />
      </div>
    ),
    className: "lg:col-start-1 lg:col-end-2 lg:row-start-1 lg:row-end-3 floating-card",
  },
  {
    Icon: User,
    name: "Human-in-the-loop",
    description:
      "Refine your research plan, or adjust focus areas all through simple natural language.",
    href: "https://github.com/bytedance/deer-flow/blob/main/src/graph/nodes.py",
    cta: "Learn more",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/20 via-teal-500/10 to-transparent opacity-60">
        <div className="absolute top-6 right-6 w-4 h-4 bg-green-400/40 rounded-full animate-ping"></div>
        <Brain className="absolute bottom-6 right-6 w-6 h-6 text-green-400/50" />
      </div>
    ),
    className: "lg:col-start-1 lg:col-end-2 lg:row-start-3 lg:row-end-4 floating-card",
  },
  {
    Icon: Bird,
    name: "Lang Stack",
    description:
      "Build with confidence using the LangChain and LangGraph frameworks.",
    href: "https://www.langchain.com/",
    cta: "Learn more",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-orange-500/20 via-yellow-500/10 to-transparent opacity-60">
        <div className="absolute top-4 left-4 w-6 h-6 bg-orange-400/30 rounded-full animate-float" style={{ animationDelay: '1s' }}></div>
        <Zap className="absolute bottom-4 right-4 w-5 h-5 text-orange-400/50" />
      </div>
    ),
    className: "lg:col-start-2 lg:col-end-3 lg:row-start-1 lg:row-end-2 floating-card",
  },
  {
    Icon: Usb,
    name: "MCP Integrations",
    description:
      "Supercharge your research workflow and expand your toolkit with seamless MCP integrations.",
    href: "https://github.com/bytedance/deer-flow/blob/main/src/graph/nodes.py",
    cta: "Learn more",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-pink-500/10 to-transparent opacity-60">
        <div className="absolute top-8 right-8 w-5 h-5 bg-purple-400/40 rounded-full animate-pulse"></div>
        <Cpu className="absolute bottom-4 left-4 w-6 h-6 text-purple-400/50" />
      </div>
    ),
    className: "lg:col-start-2 lg:col-end-3 lg:row-start-2 lg:row-end-3 floating-card",
  },
  {
    Icon: Podcast,
    name: "Podcast Generation",
    description:
      "Instantly generate podcasts from reports. Perfect for on-the-go learning or sharing findings effortlessly.",
    href: "https://github.com/bytedance/deer-flow/blob/main/src/podcast",
    cta: "Learn more",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-pink-500/20 via-rose-500/10 to-transparent opacity-60">
        <div className="absolute top-6 left-6 w-4 h-4 bg-pink-400/40 rounded-full animate-ping"></div>
        <div className="absolute bottom-8 right-8 w-3 h-3 bg-rose-400/40 rounded-full animate-float" style={{ animationDelay: '2s' }}></div>
        <Sparkles className="absolute top-12 right-12 w-4 h-4 text-pink-400/50" />
      </div>
    ),
    className: "lg:col-start-2 lg:col-end-3 lg:row-start-3 lg:row-end-4 floating-card",
  },
];

export function CoreFeatureSection() {
  return (
    <section className="relative flex w-full flex-col content-around items-center justify-center">
      {/* Enhanced background */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-pink-500/5 rounded-3xl"></div>
      
      <SectionHeader
        anchor="core-features"
        title="Core Features"
        description="Discover what makes DeerFlow the ultimate research companion"
      />
      
      <BentoGrid className="w-3/4 lg:grid-cols-2 lg:grid-rows-3 relative z-10">
        {features.map((feature, index) => (
          <div 
            key={feature.name} 
            className="animate-slide-up" 
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <BentoCard {...feature} />
          </div>
        ))}
      </BentoGrid>
    </section>
  );
}
