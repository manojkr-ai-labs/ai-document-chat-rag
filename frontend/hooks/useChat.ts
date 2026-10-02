"use client";

import { useMutation } from "@tanstack/react-query";

import { askQuestion } from "@/services/chat";

import type { ChatResponse } from "@/types/chat";

export function useChat() {
  return useMutation<
    ChatResponse,
    Error,
    {
      question: string;
      conversation_id?: string | null;
    }
  >({
    mutationFn: ({ question, conversation_id }) =>
      askQuestion(question, conversation_id),

    onSuccess: (data) => {
      console.log("Answer received:", data);
    },

    onError: (error) => {
      console.error("Chat failed:", error);
    },
  });
}