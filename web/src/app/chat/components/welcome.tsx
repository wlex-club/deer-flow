// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { motion } from "framer-motion";
import { Brain, Globe, Sparkles, Zap } from "lucide-react";

import { GradientOrb } from "~/components/magicui/gradient-orb";
import { LoadingSpinner } from "~/components/magicui/loading-spinner";
import { cn } from "~/lib/utils";

export function Welcome({ className }: { className?: string }) {
  return (
    <motion.div
      className={cn("flex flex-col relative", className)}
      style={{ transition: "all 0.2s ease-out" }}
      initial={{ opacity: 0, scale: 0.85, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      {/* Background decorations */}
      <div className="absolute inset-0 -z-10">
        <GradientOrb size="lg" color="blue" className="top-0 left-0 opacity-20" />
        <GradientOrb size="md" color="purple" className="bottom-0 right-0 opacity-20" />
      </div>
      
      {/* Enhanced welcome card */}
      <div className="relative glass-effect p-5 rounded-2xl border border-white/20 dark:border-white/10 backdrop-blur-xl shadow-lg">
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5 rounded-2xl animate-pulse opacity-50"></div>
        
        <div className="relative z-10">
          {/* Enhanced greeting with animated emoji */}
          <motion.div 
            className="mb-4 text-center"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          >
            <div className="inline-block mb-4">
              <motion.div 
                className="text-6xl"
                animate={{ rotate: [0, 10, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              >
                👋
              </motion.div>
            </div>
            <h3 className="text-3xl font-bold gradient-text text-shadow-lg">
              Hello, there!
            </h3>
          </motion.div>

          {/* Feature highlights */}
          <motion.div 
            className="flex flex-wrap justify-center gap-2 mb-3"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            <div className="flex items-center gap-2 px-3 py-2 bg-white/10 dark:bg-black/20 rounded-full backdrop-blur-sm">
              <Brain className="w-4 h-4 text-blue-500" />
              <span className="text-sm font-medium">AI Research</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-white/10 dark:bg-black/20 rounded-full backdrop-blur-sm">
              <Globe className="w-4 h-4 text-green-500" />
              <span className="text-sm font-medium">Web Search</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-white/10 dark:bg-black/20 rounded-full backdrop-blur-sm">
              <Zap className="w-4 h-4 text-purple-500" />
              <span className="text-sm font-medium">Real-time</span>
            </div>
          </motion.div>

          {/* Enhanced description */}
          <motion.div 
            className="text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.5 }}
          >
            <div className="text-muted-foreground px-2 text-sm leading-relaxed mb-3">
              Welcome to{" "}
              <motion.a
                href="https://github.com/bytedance/deer-flow"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 font-semibold gradient-text-readable hover:opacity-80 transition-all duration-300"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🦌 DeerFlow
                <Sparkles className="w-4 h-4 text-yellow-500 animate-pulse" />
              </motion.a>
              , a cutting-edge deep research assistant that helps you explore the web, 
              analyze information, and tackle complex research tasks with AI precision.
            </div>
            
            {/* Animated loading indicator */}
            <div className="flex items-center justify-center gap-3 mt-4">
              <LoadingSpinner size="sm" variant="dots" className="text-muted-foreground" />
              <span className="text-sm text-muted-foreground">
                Ready to assist you...
              </span>
            </div>
          </motion.div>
        </div>
        
        {/* Floating decorative elements */}
        <div className="absolute top-4 right-6 w-2 h-2 bg-blue-400 rounded-full animate-float"></div>
        <div className="absolute bottom-6 left-8 w-3 h-3 bg-purple-400 rounded-full animate-float" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-8 left-12 w-1 h-1 bg-pink-400 rounded-full animate-pulse"></div>
      </div>
    </motion.div>
  );
}
