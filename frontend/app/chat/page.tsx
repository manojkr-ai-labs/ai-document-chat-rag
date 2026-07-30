"use client";
import { useEffect, useRef, useState } from "react";

import ChatHistory, {
  type Message,
} from "@/components/chat/ChatHistory";
import ChatInput from "@/components/chat/ChatInput";

// import { useChat } from "@/hooks/useChat";
import ThinkingIndicator from "@/components/chat/ThinkingIndicator";
import { streamChat } from "@/services/chatStream";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  // const chatMutation = useChat();

  useEffect(() => {
  messagesEndRef.current?.scrollIntoView({
    behavior: "smooth",
  });
}, [messages]);

  const handleSend = async (question: string) => {
      // 1. User message
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);

      // 2. Create an empty assistant message
      const assistantId = crypto.randomUUID();

      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          role: "assistant",
          content: "",
          timestamp: new Date(),
        },
      ]);
      setIsStreaming(true);
      const controller = new AbortController();
      abortControllerRef.current = controller;

      try {
        // 3. Stream response
       await streamChat(
              question,
              (chunk) => {
                console.log("Chunk:", chunk);
                setMessages((prev) => {
                              const updated = prev.map((message) =>
                                message.id === assistantId
                                  ? {
                                      ...message,
                                      content: message.content + chunk,
                                    }
                                  : message
                              );

                              const assistant = updated.find(
                                (m) => m.id === assistantId
                              );

                              console.log("Assistant State:", assistant?.content);

                              return updated;
                            });
              },
              controller.signal
            );
      }  catch (error) {
            if (error instanceof DOMException && error.name === "AbortError") {
              console.log("Streaming cancelled by user.");
              return;
            }

            console.error(error);

            setMessages((prev) =>
              prev.filter((message) => message.id !== assistantId)
            );
            

            setMessages((prev) => [
              ...prev,
              {
                id: crypto.randomUUID(),
                role: "assistant",
                content: "❌ Sorry, I couldn't generate an answer.\nPlease try again.",
                timestamp: new Date(),
              },
            ]);
          }     
     finally {
        abortControllerRef.current = null;
        setIsStreaming(false);
      }
  };
  const handleStop = () => {
      abortControllerRef.current?.abort();
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
        <ChatHistory messages={messages} 
         isStreaming={isStreaming}
        />
         <div ref={messagesEndRef} />
      </div> 
      {isStreaming && <ThinkingIndicator />}
       <ChatInput
        onSend={handleSend}
        onStop={handleStop}
        isLoading={isStreaming}
      />
    </div>
  );
}