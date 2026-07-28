"use client";

import { useMutation } from "@tanstack/react-query";

import { askQuestion } from "@/services/chat";

import type { ChatResponse } from "@/types/chat";

export function useChat() {
  return useMutation<
    ChatResponse,
    Error,
    string
  >({
    mutationFn: askQuestion,

    onSuccess: (data) => {
      console.log("Answer received:", data);
    },

    onError: (error) => {
      console.error("Chat failed:", error);
    },
  });
}