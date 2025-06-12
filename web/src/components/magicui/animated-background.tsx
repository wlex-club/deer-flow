"use client";

import React, { useEffect, useRef } from "react";

interface AnimatedBackgroundProps {
  variant?: "waves" | "particles" | "grid" | "aurora";
  intensity?: "low" | "medium" | "high";
  className?: string;
}

export function AnimatedBackground({ 
  variant = "waves", 
  intensity = "medium",
  className = "" 
}: AnimatedBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let time = 0;
    const intensityMultiplier = intensity === "low" ? 0.5 : intensity === "high" ? 2 : 1;

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const drawWaves = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
      gradient.addColorStop(0, `rgba(79, 70, 229, ${0.05 * intensityMultiplier})`);
      gradient.addColorStop(0.5, `rgba(124, 58, 237, ${0.03 * intensityMultiplier})`);
      gradient.addColorStop(1, `rgba(219, 39, 119, ${0.02 * intensityMultiplier})`);
      
      ctx.fillStyle = gradient;

      for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        ctx.moveTo(0, canvas.height / 2);
        
        for (let x = 0; x < canvas.width; x += 10) {
          const y = canvas.height / 2 + 
            Math.sin((x * 0.01) + (time * 0.02) + (i * 0.5)) * 50 * intensityMultiplier +
            Math.sin((x * 0.02) + (time * 0.03) + (i * 0.3)) * 30 * intensityMultiplier;
          ctx.lineTo(x, y);
        }
        
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.fill();
      }
    };

    const drawParticles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const particleCount = 100 * intensityMultiplier;
      
      for (let i = 0; i < particleCount; i++) {
        const x = (i / particleCount) * canvas.width;
        const y = Math.sin((time * 0.01) + (i * 0.1)) * 100 + canvas.height / 2;
        const size = Math.sin((time * 0.02) + (i * 0.05)) * 3 + 2;
        const opacity = (Math.sin((time * 0.01) + (i * 0.08)) + 1) * 0.5 * intensityMultiplier;
        
        const hue = (time * 2 + i * 5) % 360;
        ctx.fillStyle = `hsla(${hue}, 70%, 60%, ${opacity})`;
        
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
      }
    };

    const drawGrid = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const gridSize = 50;
      const offset = time * 0.5;
      
      ctx.strokeStyle = `rgba(124, 58, 237, ${0.1 * intensityMultiplier})`;
      ctx.lineWidth = 1;
      
      // Vertical lines
      for (let x = 0; x < canvas.width + gridSize; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x + (offset % gridSize), 0);
        ctx.lineTo(x + (offset % gridSize), canvas.height);
        ctx.stroke();
      }
      
      // Horizontal lines
      for (let y = 0; y < canvas.height + gridSize; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y + (offset % gridSize));
        ctx.lineTo(canvas.width, y + (offset % gridSize));
        ctx.stroke();
      }
      
      // Animated intersections
      for (let x = 0; x < canvas.width + gridSize; x += gridSize) {
        for (let y = 0; y < canvas.height + gridSize; y += gridSize) {
          const pulse = Math.sin(time * 0.05 + x * 0.01 + y * 0.01) * 0.5 + 0.5;
          const size = pulse * 4 * intensityMultiplier;
          
          ctx.fillStyle = `rgba(79, 70, 229, ${pulse * 0.3 * intensityMultiplier})`;
          ctx.beginPath();
          ctx.arc(x + (offset % gridSize), y + (offset % gridSize), size, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    };

    const drawAurora = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const gradient = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 3, 0,
        canvas.width / 2, canvas.height / 3, canvas.width
      );
      
      const hue1 = (time * 2) % 360;
      const hue2 = (time * 2 + 120) % 360;
      const hue3 = (time * 2 + 240) % 360;
      
      gradient.addColorStop(0, `hsla(${hue1}, 70%, 50%, ${0.1 * intensityMultiplier})`);
      gradient.addColorStop(0.5, `hsla(${hue2}, 70%, 50%, ${0.05 * intensityMultiplier})`);
      gradient.addColorStop(1, `hsla(${hue3}, 70%, 50%, ${0.02 * intensityMultiplier})`);
      
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add flowing waves
      for (let i = 0; i < 3; i++) {
        ctx.beginPath();
        ctx.moveTo(0, canvas.height / 3);
        
        for (let x = 0; x < canvas.width; x += 5) {
          const y = canvas.height / 3 + 
            Math.sin((x * 0.005) + (time * 0.01) + (i * 2)) * 100 * intensityMultiplier;
          ctx.lineTo(x, y);
        }
        
        ctx.strokeStyle = `hsla(${(hue1 + i * 60) % 360}, 70%, 60%, ${0.3 * intensityMultiplier})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }
    };

    const animate = () => {
      time += 1;
      
      switch (variant) {
        case "waves":
          drawWaves();
          break;
        case "particles":
          drawParticles();
          break;
        case "grid":
          drawGrid();
          break;
        case "aurora":
          drawAurora();
          break;
      }
      
      animationRef.current = requestAnimationFrame(animate);
    };

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    animate();

    return () => {
      window.removeEventListener("resize", resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [variant, intensity]);

  return (
    <canvas
      ref={canvasRef}
      className={`fixed inset-0 pointer-events-none z-0 ${className}`}
      style={{ width: "100vw", height: "100vh" }}
    />
  );
} 