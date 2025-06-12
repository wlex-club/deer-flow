import React from "react";
import { cn } from "~/lib/utils";

interface GradientOrbProps {
  className?: string;
  size?: "sm" | "md" | "lg" | "xl";
  color?: "blue" | "purple" | "pink" | "green" | "orange";
  animated?: boolean;
}

const sizeClasses = {
  sm: "w-32 h-32",
  md: "w-48 h-48", 
  lg: "w-64 h-64",
  xl: "w-96 h-96",
};

const colorClasses = {
  blue: "from-blue-500/20 via-blue-400/10 to-cyan-400/20",
  purple: "from-purple-500/20 via-purple-400/10 to-pink-400/20",
  pink: "from-pink-500/20 via-rose-400/10 to-red-400/20",
  green: "from-green-500/20 via-emerald-400/10 to-teal-400/20",
  orange: "from-orange-500/20 via-yellow-400/10 to-amber-400/20",
};

export function GradientOrb({ 
  className, 
  size = "md", 
  color = "blue", 
  animated = true 
}: GradientOrbProps) {
  return (
    <div
      className={cn(
        "absolute rounded-full bg-gradient-radial blur-3xl opacity-50",
        sizeClasses[size],
        colorClasses[color],
        animated && "animate-float",
        className
      )}
    />
  );
} 