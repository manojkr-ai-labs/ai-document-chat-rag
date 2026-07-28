"use client";

import { useState } from "react";

import ChatHistory, {
  type Message,
} from "@/components/chat/ChatHistory";
import ChatInput from "@/components/chat/ChatInput";

import { useChat } from "@/hooks/useChat";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);

  const chatMutation = useChat();

  const handleSend = async (question: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await chatMutation.mutateAsync(
        question
      );

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="mx-auto flex h-[calc(100vh-100px)] max-w-5xl flex-col gap-6 p-6">
      <div>
        <h1 className="text-3xl font-bold">
          AI Document Chat
        </h1>

        <p className="mt-2 text-gray-500">
          Ask questions about your indexed PDF documents.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto rounded-xl border bg-slate-50 p-6">
        <ChatHistory messages={messages} />
      </div>

      <ChatInput
        onSend={handleSend}
        isLoading={chatMutation.isPending}
      />
    </div>
  );
}