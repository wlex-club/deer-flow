// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

import { motion } from "framer-motion";

import { cn } from "~/lib/utils";

import { Welcome } from "./welcome";

const questions = [
  "How many times taller is the Eiffel Tower than the tallest building in the world?",
  "How many years does an average Tesla battery last compared to a gasoline engine?",
  "How many liters of water are required to produce 1 kg of beef?",
  "How many times faster is the speed of light compared to the speed of sound?",
];
export function ConversationStarter({
  className,
  onSend,
}: {
  className?: string;
  onSend?: (message: string) => void;
}) {
  return (
    <div className={cn("flex flex-col items-center space-y-6 w-full", className)}>
      <Welcome className="w-full max-w-3xl" />
      <div className="w-full">
        <ul className="flex flex-wrap gap-4">
        {questions.map((question, index) => (
          <motion.li
            key={question}
            className="flex w-[calc(50%-8px)] shrink-0 active:scale-105"
            style={{ transition: "all 0.2s ease-out" }}
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{
              duration: 0.2,
              delay: index * 0.1 + 0.5,
              ease: "easeOut",
            }}
          >
            <div
              className="bg-card text-foreground cursor-pointer rounded-2xl border px-4 py-4 transition-all duration-300 hover:bg-accent hover:shadow-lg shadow-sm w-full"
              onClick={() => {
                onSend?.(question);
              }}
            >
              {question}
            </div>
          </motion.li>
        ))}
        </ul>
      </div>
    </div>
  );
}
