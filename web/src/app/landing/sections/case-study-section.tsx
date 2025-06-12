// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { Bike, Building, Film, Github, Ham, Home, Pizza, Sparkles, PlayCircle } from "lucide-react";
import { Bot } from "lucide-react";

import { BentoCard } from "~/components/magicui/bento-grid";
import { FloatingParticles } from "~/components/magicui/floating-particles";
import { GradientOrb } from "~/components/magicui/gradient-orb";

import { SectionHeader } from "../components/section-header";

const caseStudies = [
  {
    id: "eiffel-tower-vs-tallest-building",
    icon: Building,
    title: "How tall is Eiffel Tower compared to tallest building?",
    description:
      "The research compares the heights and global significance of the Eiffel Tower and Burj Khalifa, and uses Python code to calculate the multiples.",
    color: "blue",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/15 via-blue-400/8 to-transparent opacity-80">
        <div className="absolute top-3 right-3 w-6 h-6 bg-blue-400/20 rounded-full animate-pulse"></div>
        <Building className="absolute bottom-3 left-3 w-5 h-5 text-blue-400/40" />
      </div>
    ),
  },
  {
    id: "github-top-trending-repo",
    icon: Github,
    title: "What are the top trending repositories on GitHub?",
    description:
      "The research utilized MCP services to identify the most popular GitHub repositories and documented them in detail using search engines.",
    color: "purple",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/15 via-purple-400/8 to-transparent opacity-80">
        <div className="absolute top-4 left-4 w-4 h-4 bg-purple-400/25 rounded-full animate-float"></div>
        <Github className="absolute bottom-3 right-3 w-5 h-5 text-purple-400/40" />
      </div>
    ),
  },
  {
    id: "nanjing-traditional-dishes",
    icon: Ham,
    title: "Write an article about Nanjing's traditional dishes",
    description:
      "The study vividly showcases Nanjing's famous dishes through rich content and imagery, uncovering their hidden histories and cultural significance.",
    color: "orange",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-orange-500/15 via-orange-400/8 to-transparent opacity-80">
        <div className="absolute top-2 right-4 w-3 h-3 bg-orange-400/30 rounded-full animate-ping"></div>
        <Ham className="absolute bottom-4 left-4 w-5 h-5 text-orange-400/40" />
      </div>
    ),
  },
  {
    id: "rental-apartment-decoration",
    icon: Home,
    title: "How to decorate a small rental apartment?",
    description:
      "The study provides readers with practical and straightforward methods for decorating apartments, accompanied by inspiring images.",
    color: "green",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/15 via-green-400/8 to-transparent opacity-80">
        <div className="absolute top-5 left-5 w-5 h-5 bg-green-400/20 rounded-full animate-float" style={{ animationDelay: '1s' }}></div>
        <Home className="absolute bottom-3 right-3 w-5 h-5 text-green-400/40" />
      </div>
    ),
  },
  {
    id: "review-of-the-professional",
    icon: Film,
    title: "Introduce the movie 'Léon: The Professional'",
    description:
      "The research provides a comprehensive introduction to the movie 'Léon: The Professional', including its plot, characters, and themes.",
    color: "pink",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-pink-500/15 via-pink-400/8 to-transparent opacity-80">
        <div className="absolute top-3 left-6 w-4 h-4 bg-pink-400/25 rounded-full animate-pulse"></div>
        <Film className="absolute bottom-4 right-4 w-5 h-5 text-pink-400/40" />
      </div>
    ),
  },
  {
    id: "china-food-delivery",
    icon: Bike,
    title: "How do you view the takeaway war in China? (in Chinese)",
    description:
      "The research analyzes the intensifying competition between JD and Meituan, highlighting their strategies, technological innovations, and challenges.",
    color: "indigo",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/15 via-indigo-400/8 to-transparent opacity-80">
        <div className="absolute top-4 right-2 w-3 h-3 bg-indigo-400/30 rounded-full animate-float" style={{ animationDelay: '2s' }}></div>
        <Bike className="absolute bottom-3 left-3 w-5 h-5 text-indigo-400/40" />
      </div>
    ),
  },
  {
    id: "ultra-processed-foods",
    icon: Pizza,
    title: "Are ultra-processed foods linked to health?",
    description:
      "The research examines the health risks of rising ultra-processed food consumption, urging more research on long-term effects and individual differences.",
    color: "red",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-red-500/15 via-red-400/8 to-transparent opacity-80">
        <div className="absolute top-6 left-3 w-4 h-4 bg-red-400/25 rounded-full animate-ping"></div>
        <Pizza className="absolute bottom-3 right-3 w-5 h-5 text-red-400/40" />
      </div>
    ),
  },
  {
    id: "ai-twin-insurance",
    icon: Bot,
    title: 'Write an article on "Would you insure your AI twin?"',
    description:
      "The research explores the concept of insuring AI twins, highlighting their benefits, risks, ethical considerations, and the evolving regulatory.",
    color: "cyan",
    background: (
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/15 via-cyan-400/8 to-transparent opacity-80">
        <div className="absolute top-3 right-5 w-5 h-5 bg-cyan-400/20 rounded-full animate-float" style={{ animationDelay: '0.5s' }}></div>
        <Bot className="absolute bottom-4 left-4 w-5 h-5 text-cyan-400/40" />
      </div>
    ),
  },
];

export function CaseStudySection() {
  return (
    <section className="relative container flex flex-col items-center justify-center py-16">
      {/* Enhanced background */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-muted/10 to-transparent rounded-3xl"></div>
      
      {/* Background decorations */}
      <GradientOrb size="lg" color="blue" className="top-10 left-10 opacity-30" />
      <GradientOrb size="md" color="purple" className="bottom-20 right-20 opacity-30" />
      <FloatingParticles count={20} className="opacity-40" />
      
      <div className="relative z-10 w-full">
        <SectionHeader
          anchor="case-studies"
          title="Case Studies"
          description="Explore real-world examples of DeerFlow's research capabilities through interactive replays"
        />
        
        {/* Enhanced grid with staggered animations */}
        <div className="grid grid-cols-1 gap-6 max-w-7xl mx-auto sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {caseStudies.map((caseStudy, index) => (
            <div 
              key={caseStudy.title} 
              className="w-full animate-slide-up hover-lift"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="relative group">
                {/* Enhanced BentoCard with custom styling */}
                <BentoCard
                  {...{
                    Icon: caseStudy.icon,
                    name: caseStudy.title,
                    description: caseStudy.description,
                    href: `/chat?replay=${caseStudy.id}`,
                    cta: "Watch Replay",
                    className: "w-full h-full floating-card glass-effect border-2 border-white/10 hover:border-white/20 transition-all duration-300",
                    background: caseStudy.background,
                  }}
                />
                
                {/* Play button overlay */}
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="flex items-center gap-1 px-2 py-1 bg-white/10 dark:bg-black/20 backdrop-blur-sm rounded-full text-xs">
                    <PlayCircle className="w-3 h-3" />
                    <span>Play</span>
                  </div>
                </div>
                
                {/* Shimmer effect on hover */}
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -skew-x-12 animate-shine"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Bottom decoration */}
        <div className="flex justify-center mt-12">
          <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-full border border-white/10">
            <Sparkles className="w-4 h-4 text-blue-500 animate-pulse" />
            <span className="text-sm text-muted-foreground">Click any case to explore the research process</span>
            <Sparkles className="w-4 h-4 text-purple-500 animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  );
}
