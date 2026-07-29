"use client";
import { useEffect, useRef, useState } from "react";

import ChatHistory, {
  type Message,
} from "@/components/chat/ChatHistory";
import ChatInput from "@/components/chat/ChatInput";

import { useChat } from "@/hooks/useChat";
import ThinkingIndicator from "@/components/chat/ThinkingIndicator";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatMutation = useChat();

  useEffect(() => {
  messagesEndRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);

  const handleSend = async (question: string) => {
   
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
        timestamp: new Date(),
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
            timestamp: new Date(),
            citations: response.data.citations
            };

      setMessages((prev) => [
        ...prev,
        assistantMessage,
      ]);
    }  catch (error) {
        console.error(error);

        const errorMessage: Message = {
            id: crypto.randomUUID(),
            role: "assistant",
            content:
            `❌ Sorry, I couldn't generate an answer.\n Please try again.`,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, errorMessage]);
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
         <div ref={messagesEndRef} />
      </div>
      {chatMutation.isPending && <ThinkingIndicator />}
        <ChatInput
        onSend={handleSend}
        isLoading={chatMutation.isPending}
        /> 
    </div>
  );
}