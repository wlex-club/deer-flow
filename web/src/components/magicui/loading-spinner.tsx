import React from "react";
import { cn } from "~/lib/utils";

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "pulse" | "spin" | "bounce" | "wave" | "dots";
  className?: string;
}

const sizeClasses = {
  sm: "w-4 h-4",
  md: "w-8 h-8", 
  lg: "w-12 h-12",
  xl: "w-16 h-16",
};

export function LoadingSpinner({ 
  size = "md", 
  variant = "spin", 
  className 
}: LoadingSpinnerProps) {
  
  if (variant === "pulse") {
    return (
      <div className={cn("relative", sizeClasses[size], className)}>
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 animate-pulse"></div>
        <div className="absolute inset-1 rounded-full bg-background"></div>
        <div className="absolute inset-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-pulse" style={{ animationDelay: '0.5s' }}></div>
      </div>
    );
  }
  
  if (variant === "bounce") {
    return (
      <div className={cn("flex space-x-1", className)}>
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-3 h-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.1}s` }}
          />
        ))}
      </div>
    );
  }
  
  if (variant === "wave") {
    return (
      <div className={cn("flex items-end space-x-1", className)}>
        {[0, 1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="w-2 bg-gradient-to-t from-blue-500 to-purple-500 rounded-full animate-pulse"
            style={{ 
              height: `${8 + (i % 2) * 8}px`,
              animationDelay: `${i * 0.1}s`,
              animationDuration: '1s'
            }}
          />
        ))}
      </div>
    );
  }
  
  if (variant === "dots") {
    return (
      <div className={cn("flex space-x-2", className)}>
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full animate-pulse"
            style={{ 
              background: `linear-gradient(135deg, hsl(${220 + i * 30}, 70%, 60%) 0%, hsl(${250 + i * 30}, 70%, 70%) 100%)`,
              animationDelay: `${i * 0.2}s`
            }}
          />
        ))}
      </div>
    );
  }
  
  // Default spin variant
  return (
    <div className={cn("relative", sizeClasses[size], className)}>
      <div className="absolute inset-0 rounded-full border-4 border-gray-200 dark:border-gray-700"></div>
      <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-500 border-r-purple-500 animate-spin"></div>
      <div className="absolute inset-1 rounded-full border-2 border-transparent border-b-pink-500 border-l-cyan-500 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '0.8s' }}></div>
    </div>
  );
} 