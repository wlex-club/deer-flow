import React from "react";

interface FloatingParticlesProps {
  count?: number;
  className?: string;
}

export function FloatingParticles({ count = 50, className = "" }: FloatingParticlesProps) {
  const particles = Array.from({ length: count }, (_, i) => (
    <div
      key={i}
      className={`absolute w-1 h-1 bg-gradient-to-r from-blue-400/30 to-purple-400/30 rounded-full animate-float opacity-50 ${className}`}
      style={{
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        animationDelay: `${Math.random() * 6}s`,
        animationDuration: `${4 + Math.random() * 4}s`,
      }}
    />
  ));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles}
    </div>
  );
} 