import {api} from "./api";

import type {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";

export async function askQuestion(
  question: string
) {
  const payload: ChatRequest = {
    question,
  };

  const response = await api.post<ChatResponse>(
    "/chat",
    payload
  );

  return response.data;
}