// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { motion } from "framer-motion";
import { FastForward, Play, Sparkles, Zap } from "lucide-react";
import { useCallback, useRef, useState } from "react";

import { RainbowText } from "~/components/deer-flow/rainbow-text";
import { LoadingSpinner } from "~/components/magicui/loading-spinner";
import { Button } from "~/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "~/components/ui/card";
import { fastForwardReplay } from "~/core/api";
import { useReplayMetadata } from "~/core/api/hooks";
import type { Option, Resource } from "~/core/messages";
import { useReplay } from "~/core/replay";
import { sendMessage, useMessageIds, useStore } from "~/core/store";
import { env } from "~/env";
import { cn } from "~/lib/utils";

import { ConversationStarter } from "./conversation-starter";
import { InputBox } from "./input-box";
import { MessageListView } from "./message-list-view";
import { Welcome } from "./welcome";

export function MessagesBlock({ className }: { className?: string }) {
  const messageIds = useMessageIds();
  const messageCount = messageIds.length;
  const responding = useStore((state) => state.responding);
  const { isReplay } = useReplay();
  const { title: replayTitle, hasError: replayHasError } = useReplayMetadata();
  const [replayStarted, setReplayStarted] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const [feedback, setFeedback] = useState<{ option: Option } | null>(null);
  const handleSend = useCallback(
    async (
      message: string,
      options?: {
        interruptFeedback?: string;
        resources?: Array<Resource>;
      },
    ) => {
      const abortController = new AbortController();
      abortControllerRef.current = abortController;
      try {
        await sendMessage(
          message,
          {
            interruptFeedback:
              options?.interruptFeedback ?? feedback?.option.value,
            resources: options?.resources,
          },
          {
            abortSignal: abortController.signal,
          },
        );
      } catch {}
    },
    [feedback],
  );
  const handleCancel = useCallback(() => {
    abortControllerRef.current?.abort();
    abortControllerRef.current = null;
  }, []);
  const handleFeedback = useCallback(
    (feedback: { option: Option }) => {
      setFeedback(feedback);
    },
    [setFeedback],
  );
  const handleRemoveFeedback = useCallback(() => {
    setFeedback(null);
  }, [setFeedback]);
  const handleStartReplay = useCallback(() => {
    setReplayStarted(true);
    void sendMessage();
  }, [setReplayStarted]);
  const [fastForwarding, setFastForwarding] = useState(false);
  const handleFastForwardReplay = useCallback(() => {
    setFastForwarding(!fastForwarding);
    fastForwardReplay(!fastForwarding);
  }, [fastForwarding]);
  return (
    <div className={cn("flex h-full flex-col relative", className)}>
      {/* Background enhancement */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/30 via-purple-50/20 to-pink-50/30 dark:from-blue-950/20 dark:via-purple-950/10 dark:to-pink-950/20 rounded-xl opacity-60"></div>
      
      {!isReplay ? (
        messageCount === 0 && !responding ? (
          /* 初始状态：显示Welcome和问题卡片 */
          <div className="flex flex-col h-full justify-center items-center px-4 relative z-10">
            <ConversationStarter
              className="w-full max-w-4xl mb-8"
              onSend={handleSend}
            />
            {/* Enhanced input box with glow effect - 宽度与上面的卡片保持一致，并增加高度 */}
            <div className="relative w-full max-w-4xl h-32">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-2xl blur-lg opacity-50"></div>
              <InputBox
                className="h-full w-full relative z-10"
                responding={responding}
                feedback={feedback}
                onSend={handleSend}
                onCancel={handleCancel}
                onRemoveFeedback={handleRemoveFeedback}
              />
            </div>
          </div>
        ) : (
          /* 聊天状态：显示消息列表和输入框 */
          <>
            <MessageListView
              className="flex flex-grow relative z-10"
              onFeedback={handleFeedback}
              onSendMessage={handleSend}
            />
            <div className="relative flex h-36 shrink-0 pb-4 z-10">
              {/* Enhanced input box with glow effect - 增加高度保持一致 */}
              <div className="relative w-full h-full">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-2xl blur-lg opacity-50"></div>
                <InputBox
                  className="h-full w-full relative z-10"
                  responding={responding}
                  feedback={feedback}
                  onSend={handleSend}
                  onCancel={handleCancel}
                  onRemoveFeedback={handleRemoveFeedback}
                />
              </div>
            </div>
          </>
        )
      ) : (
        <>
          <div
            className={cn(
              "fixed bottom-[calc(50vh+80px)] left-0 transition-all duration-500 ease-out",
              replayStarted && "pointer-events-none scale-150 opacity-0",
            )}
          >
            <Welcome />
          </div>
          <motion.div
            className="mb-4 h-fit w-full items-center justify-center z-10"
            initial={{ opacity: 0, y: "20vh" }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            {/* Enhanced card with glass morphism */}
            <Card
              className={cn(
                "w-full transition-all duration-300 glass-effect border-2 border-white/20 dark:border-white/10 backdrop-blur-xl",
                !replayStarted && "translate-y-[-40vh]",
                responding && "glow-effect"
              )}
            >
              <div className="flex items-center justify-between relative">
                {/* Animated background pattern */}
                {responding && (
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 via-purple-500/5 to-pink-500/5 animate-pulse rounded-lg"></div>
                )}
                
                <div className="flex flex-grow items-center relative z-10">
                  {responding && (
                    <motion.div
                      className="ml-3 relative"
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.8 }}
                      transition={{ duration: 0.3 }}
                    >
                      {/* Enhanced deer animation with glow */}
                      <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-full blur-md animate-pulse"></div>
                        <video
                          // Walking deer animation, designed by @liangzhaojun. Thank you for creating it!
                          src="/images/walking_deer.webm"
                          autoPlay
                          loop
                          muted
                          className="h-[42px] w-[42px] object-contain relative z-10 drop-shadow-lg"
                        />
                      </div>
                    </motion.div>
                  )}
                  <CardHeader className={cn("flex-grow", responding && "pl-3")}>
                    <CardTitle className="flex items-center gap-2">
                      <RainbowText animated={responding}>
                        {responding ? "Replaying" : `${replayTitle}`}
                      </RainbowText>
                      {responding && (
                        <LoadingSpinner size="sm" variant="dots" />
                      )}
                    </CardTitle>
                    <CardDescription className="flex items-center gap-2">
                      <RainbowText animated={responding}>
                        {responding
                          ? "DeerFlow is now replaying the conversation..."
                          : replayStarted
                            ? "The replay has been stopped."
                            : `You're now in DeerFlow's replay mode. Click the "Play" button on the right to start.`}
                      </RainbowText>
                      {!responding && !replayStarted && (
                        <Sparkles className="w-4 h-4 text-blue-500 animate-pulse" />
                      )}
                    </CardDescription>
                  </CardHeader>
                </div>
                {!replayHasError && (
                  <div className="pr-4 relative z-10">
                    {responding && (
                      <Button
                        className={cn(
                          "hover-lift transition-all duration-300 group",
                          fastForwarding && "animate-pulse bg-gradient-to-r from-blue-500 to-purple-500"
                        )}
                        variant={fastForwarding ? "default" : "outline"}
                        onClick={handleFastForwardReplay}
                      >
                        <Zap className={cn("w-4 h-4 mr-2", fastForwarding && "animate-bounce")} />
                        Fast Forward
                        {fastForwarding && (
                          <div className="absolute inset-0 bg-gradient-to-r from-blue-400/20 to-purple-400/20 rounded-md blur-sm animate-pulse"></div>
                        )}
                      </Button>
                    )}
                    {!replayStarted && (
                      <Button 
                        className="w-24 hover-lift bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 transition-all duration-300 group"
                        onClick={handleStartReplay}
                      >
                        <Play className="w-4 h-4 mr-1 group-hover:animate-pulse" />
                        Play
                      </Button>
                    )}
                  </div>
                )}
              </div>
            </Card>
            {!replayStarted && env.NEXT_PUBLIC_STATIC_WEBSITE_ONLY && (
              <div className="text-muted-foreground w-full text-center text-xs mt-4 p-3 bg-white/5 dark:bg-black/10 backdrop-blur-sm rounded-lg border border-white/10">
                <Sparkles className="w-3 h-3 inline mr-1 text-yellow-500" />
                This site is for demo purposes only. If you want to try your
                own question, please{" "}
                <a
                  className="underline hover:text-blue-500 transition-colors duration-200"
                  href="https://github.com/bytedance/deer-flow"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  visit our GitHub repository
                </a>
                .
              </div>
            )}
          </motion.div>
        </>
      )}
    </div>
  );
}
