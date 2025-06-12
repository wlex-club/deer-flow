// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { MagicWandIcon } from "@radix-ui/react-icons";
import { AnimatePresence, motion } from "framer-motion";
import { ArrowUp, X } from "lucide-react";
import { useCallback, useRef, useState } from "react";

import { Detective } from "~/components/deer-flow/icons/detective";
import MessageInput, {
  type MessageInputRef,
} from "~/components/deer-flow/message-input";
import { ReportStyleDialog } from "~/components/deer-flow/report-style-dialog";
import { Tooltip } from "~/components/deer-flow/tooltip";
import { BorderBeam } from "~/components/magicui/border-beam";
import { Button } from "~/components/ui/button";
import { enhancePrompt } from "~/core/api";
import type { Option, Resource } from "~/core/messages";
import {
  setEnableBackgroundInvestigation,
  useSettingsStore,
} from "~/core/store";
import { cn } from "~/lib/utils";

export function InputBox({
  className,
  responding,
  feedback,
  onSend,
  onCancel,
  onRemoveFeedback,
}: {
  className?: string;
  size?: "large" | "normal";
  responding?: boolean;
  feedback?: { option: Option } | null;
  onSend?: (
    message: string,
    options?: {
      interruptFeedback?: string;
      resources?: Array<Resource>;
    },
  ) => void;
  onCancel?: () => void;
  onRemoveFeedback?: () => void;
}) {
  const backgroundInvestigation = useSettingsStore(
    (state) => state.general.enableBackgroundInvestigation,
  );
  const reportStyle = useSettingsStore((state) => state.general.reportStyle);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<MessageInputRef>(null);
  const feedbackRef = useRef<HTMLDivElement>(null);

  // Enhancement state
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [isEnhanceAnimating, setIsEnhanceAnimating] = useState(false);
  const [currentPrompt, setCurrentPrompt] = useState("");

  const handleSendMessage = useCallback(
    (message: string, resources: Array<Resource>) => {
      if (responding) {
        onCancel?.();
      } else {
        if (message.trim() === "") {
          return;
        }
        if (onSend) {
          onSend(message, {
            interruptFeedback: feedback?.option.value,
            resources,
          });
          onRemoveFeedback?.();
          // Clear enhancement animation after sending
          setIsEnhanceAnimating(false);
        }
      }
    },
    [responding, onCancel, onSend, feedback, onRemoveFeedback],
  );

  const handleEnhancePrompt = useCallback(async () => {
    if (currentPrompt.trim() === "" || isEnhancing) {
      return;
    }

    setIsEnhancing(true);
    setIsEnhanceAnimating(true);

    try {
      const enhancedPrompt = await enhancePrompt({
        prompt: currentPrompt,
        report_style: reportStyle.toUpperCase(),
      });

      // Add a small delay for better UX
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Update the input with the enhanced prompt with animation
      if (inputRef.current) {
        inputRef.current.setContent(enhancedPrompt);
        setCurrentPrompt(enhancedPrompt);
      }

      // Keep animation for a bit longer to show the effect
      setTimeout(() => {
        setIsEnhanceAnimating(false);
      }, 1000);
    } catch (error) {
      console.error("Failed to enhance prompt:", error);
      setIsEnhanceAnimating(false);
      // Could add toast notification here
    } finally {
      setIsEnhancing(false);
    }
  }, [currentPrompt, isEnhancing, reportStyle]);

  return (
    <div
      className={cn(
        "bg-card text-foreground relative flex h-full w-full flex-col rounded-[24px] border border-border shadow-sm overflow-hidden",
        className,
      )}
      ref={containerRef}
    >
      <div className="relative flex-1 flex flex-col">
        <AnimatePresence>
          {feedback && (
            <motion.div
              ref={feedbackRef}
              className="bg-background border-brand absolute top-0 left-0 mt-2 ml-4 flex items-center justify-center gap-1 rounded-2xl border px-2 py-0.5 z-10"
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0 }}
              transition={{ duration: 0.2, ease: "easeInOut" }}
            >
              <div className="text-brand flex h-full w-full items-center justify-center text-sm font-medium">
                {feedback.option.text}
              </div>
              <X
                className="cursor-pointer text-muted-foreground hover:text-foreground transition-colors"
                size={16}
                onClick={onRemoveFeedback}
              />
            </motion.div>
          )}
          {isEnhanceAnimating && (
            <motion.div
              className="pointer-events-none absolute inset-0 z-20"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="relative h-full w-full">
                {/* Sparkle effect overlay */}
                <motion.div
                  className="absolute inset-0 rounded-[24px] bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-blue-500/10"
                  animate={{
                    background: [
                      "linear-gradient(45deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1), rgba(59, 130, 246, 0.1))",
                      "linear-gradient(225deg, rgba(147, 51, 234, 0.1), rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1))",
                      "linear-gradient(45deg, rgba(59, 130, 246, 0.1), rgba(147, 51, 234, 0.1), rgba(59, 130, 246, 0.1))",
                    ],
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
                {/* Floating sparkles */}
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute h-2 w-2 rounded-full bg-blue-400"
                    style={{
                      left: `${20 + i * 12}%`,
                      top: `${30 + (i % 2) * 40}%`,
                    }}
                    animate={{
                      y: [-10, -20, -10],
                      opacity: [0, 1, 0],
                      scale: [0.5, 1, 0.5],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      delay: i * 0.2,
                    }}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        
        {/* 输入区域 - 使用相对定位容器 */}
        <div className="relative flex-1">
          <MessageInput
            className={cn("h-full px-4 pt-6 pb-14", feedback && "pt-10")}
            ref={inputRef}
            onEnter={handleSendMessage}
            onChange={setCurrentPrompt}
          />
          
          {/* 内嵌按钮区域 - 绝对定位在输入框内部底部 */}
          <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between px-4 py-2 bg-gradient-to-t from-card via-card/95 to-transparent">
            <div className="flex items-center gap-2">
              <Tooltip
                className="max-w-60"
                title={
                  <div>
                    <h3 className="mb-2 font-bold">
                      Investigation Mode: {backgroundInvestigation ? "On" : "Off"}
                    </h3>
                    <p>
                      When enabled, DeerFlow will perform a quick search before
                      planning. This is useful for researches related to ongoing
                      events and news.
                    </p>
                  </div>
                }
              >
                <Button
                  size="sm"
                  className={cn(
                    "rounded-2xl h-8 px-3 text-xs font-medium transition-all active:scale-95 backdrop-blur-sm",
                    backgroundInvestigation 
                      ? "!border-brand !text-brand bg-brand/5 hover:bg-brand/10" 
                      : "bg-background/60 hover:bg-background/80"
                  )}
                  variant="outline"
                  onClick={() =>
                    setEnableBackgroundInvestigation(!backgroundInvestigation)
                  }
                >
                  <Detective className="w-3 h-3" /> 
                  <span className="ml-1">Investigation</span>
                </Button>
              </Tooltip>
              <ReportStyleDialog />
            </div>
            
            <div className="flex items-center gap-2">
              <Tooltip title="Enhance prompt with AI">
                <Button
                  variant="ghost"
                  size="icon"
                  className={cn(
                    "hover:bg-accent h-8 w-8 backdrop-blur-sm",
                    isEnhancing && "animate-pulse",
                  )}
                  onClick={handleEnhancePrompt}
                  disabled={isEnhancing || currentPrompt.trim() === ""}
                >
                  {isEnhancing ? (
                    <div className="flex h-8 w-8 items-center justify-center">
                      <div className="bg-foreground h-3 w-3 animate-bounce rounded-full opacity-70" />
                    </div>
                  ) : (
                    <MagicWandIcon className="text-brand" />
                  )}
                </Button>
              </Tooltip>
              <Tooltip title={responding ? "Stop" : "Send"}>
                <Button
                  variant="outline"
                  size="icon"
                  className={cn(
                    "h-8 w-8 rounded-full transition-all active:scale-95 backdrop-blur-sm",
                    responding 
                      ? "bg-destructive/10 hover:bg-destructive/20 border-destructive/20" 
                      : "bg-brand/5 hover:bg-brand/10 border-brand/20"
                  )}
                  onClick={() => inputRef.current?.submit()}
                >
                  {responding ? (
                    <div className="flex h-8 w-8 items-center justify-center">
                      <div className="bg-destructive h-3 w-3 rounded-sm" />
                    </div>
                  ) : (
                    <ArrowUp className="w-4 h-4 text-brand" />
                  )}
                </Button>
              </Tooltip>
            </div>
          </div>
        </div>
      </div>
      {isEnhancing && (
        <>
          <BorderBeam
            duration={5}
            size={250}
            className="from-transparent via-red-500 to-transparent"
          />
          <BorderBeam
            duration={5}
            delay={3}
            size={250}
            className="from-transparent via-blue-500 to-transparent"
          />
        </>
      )}
    </div>
  );
}
