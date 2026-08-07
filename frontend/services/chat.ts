import {api} from "./api";

import type {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";

export async function askQuestion(
  question: string,
  conversation_id?: string | null,
)
 {
  const payload: ChatRequest = {
    question,
    conversation_id: conversation_id ?? undefined,
  };

  const response = await api.post<ChatResponse>(
    "/chat",
    payload
  );

  return response.data;
}