// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { AnimatePresence, motion } from "framer-motion";
import { ArrowUp, X } from "lucide-react";
import { useCallback, useRef } from "react";

import { Detective } from "~/components/deer-flow/icons/detective";
import MessageInput, {
  type MessageInputRef,
} from "~/components/deer-flow/message-input";
import { Tooltip } from "~/components/deer-flow/tooltip";
import { Button } from "~/components/ui/button";
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
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<MessageInputRef>(null);
  const feedbackRef = useRef<HTMLDivElement>(null);

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
        }
      }
    },
    [responding, onCancel, onSend, feedback, onRemoveFeedback],
  );

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
        </AnimatePresence>
        
        {/* 输入区域 - 使用相对定位容器 */}
        <div className="relative flex-1">
          <MessageInput
            className={cn("h-full px-4 pt-6 pb-14", feedback && "pt-10")}
            ref={inputRef}
            onEnter={handleSendMessage}
          />
          
          {/* 内嵌按钮区域 - 绝对定位在输入框内部底部 */}
          <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between px-4 py-2 bg-gradient-to-t from-card via-card/95 to-transparent">
            <div className="flex items-center">
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
            </div>
            
            <div className="flex items-center">
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
    </div>
  );
}
