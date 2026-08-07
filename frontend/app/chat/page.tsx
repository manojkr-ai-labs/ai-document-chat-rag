"use client";

import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import ChatHistory, {
  type Message,
} from "@/components/chat/ChatHistory";

import ChatInput from "@/components/chat/ChatInput";
import ThinkingIndicator from "@/components/chat/ThinkingIndicator";
import ConversationSidebar from "@/components/sidebar/ConversationSidebar";

import { useConversation } from "@/hooks/useConversation";
import { askQuestion } from "@/services/chat";

function mapMessages(rawMessages: any[] = []): Message[] {
  return rawMessages.map((message) => ({
    id: String(message.id),
    role: message.role,
    content: message.content ?? "",
    timestamp: message.created_at
      ? new Date(message.created_at)
      : new Date(),
    citations: message.citations ?? undefined,
  }));
}

export default function ChatPage() {
  const queryClient = useQueryClient();

  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [selectedConversationId, setSelectedConversationId] =
    useState<string>();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  // Ignore stale loads when the user clicks chats quickly
  const loadRequestIdRef = useRef(0);

  const {
    data: conversationResponse,
    isPending: isConversationPending,
    isError: isConversationError,
    isFetching: isConversationFetching,
  } = useConversation(selectedConversationId);

  const isLoadingConversation = Boolean(
    selectedConversationId &&
      !isConversationError &&
      (isConversationPending ||
        (isConversationFetching && messages.length === 0))
  );

  // Load history whenever the selected conversation (or its data) changes
  useEffect(() => {
    if (!selectedConversationId) {
      setMessages([]);
      return;
    }

    if (isStreaming) return;

    if (isConversationPending) {
      setMessages([]);
      return;
    }

    if (isConversationError) {
      setMessages([]);
      return;
    }

    const body = conversationResponse as any;
    // Support both { data: { messages } } and { messages }
    const rawMessages =
      body?.data?.messages ?? body?.messages ?? null;

    if (rawMessages == null) return;

    const requestId = ++loadRequestIdRef.current;
    const next = mapMessages(rawMessages);

    if (requestId === loadRequestIdRef.current) {
      setMessages(next);
    }
  }, [
    selectedConversationId,
    conversationResponse,
    isConversationPending,
    isConversationError,
    isStreaming,
  ]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const handleSelectConversation = (id: string) => {
    if (id === selectedConversationId) return;
    setMessages([]);
    setSelectedConversationId(id);
  };

  const handleNewChatStarted = () => {
    setMessages([]);
    setSelectedConversationId(undefined);
  };

  const handleSend = async (question: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      timestamp: new Date(),
    };

    const assistantId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        id: assistantId,
        role: "assistant",
        content: "",
        timestamp: new Date(),
      },
    ]);

    setIsStreaming(true);

    try {
      const response = await askQuestion(
        question,
        selectedConversationId ?? null
      );

      const conversationId = response.data.conversation_id;
      const answer = response.data.answer;
      const citations = response.data.citations ?? [];

      if (!conversationId) {
        throw new Error("No conversation_id in chat response");
      }

      const nextMessages: Message[] = [
        ...messages,
        userMessage,
        {
          id: assistantId,
          role: "assistant",
          content: answer,
          timestamp: new Date(),
          citations,
        },
      ];

      setMessages(nextMessages);

      queryClient.setQueryData(["conversation", conversationId], {
        success: true,
        data: {
          id: conversationId,
          messages: nextMessages.map((message) => ({
            id: message.id,
            role: message.role,
            content: message.content,
            created_at: message.timestamp.toISOString(),
            citations: message.citations ?? null,
          })),
        },
      });

      setSelectedConversationId(conversationId);

      await queryClient.invalidateQueries({
        queryKey: ["conversations"],
      });
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev.filter((message) => message.id !== assistantId),
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "❌ Sorry, I couldn't generate an answer.\nPlease try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex h-screen">
      <ConversationSidebar
        selectedConversationId={selectedConversationId}
        onSelectConversation={handleSelectConversation}
        onNewChatStarted={handleNewChatStarted}
      />

      <div className="flex flex-1 flex-col">
        <div className="mx-auto flex h-[calc(100vh-100px)] max-w-5xl flex-col gap-6 p-6">
          <div>
            <h1 className="text-3xl font-bold">
              AI Document Chat
            </h1>

            <p className="mt-2 text-gray-500">
              Ask questions about your indexed PDF
              documents.
            </p>
          </div>

          <div className="flex-1 overflow-y-auto rounded-xl border bg-slate-50 p-6">
            {isConversationError && selectedConversationId ? (
              <div className="rounded-xl border border-dashed p-10 text-center text-red-500">
                <h3 className="text-lg font-semibold">
                  Could not load this chat
                </h3>
                <p className="mt-2 text-sm">
                  Try selecting it again from the sidebar.
                </p>
              </div>
            ) : (
              <ChatHistory
                messages={messages}
                isStreaming={isStreaming}
                isLoading={isLoadingConversation}
              />
            )}

            <div ref={messagesEndRef} />
          </div>

          {isStreaming && <ThinkingIndicator />}

          <ChatInput
            onSend={handleSend}
            onStop={() => {}}
            isStreaming={isStreaming}
            disabled={isLoadingConversation}
          />
        </div>
      </div>
    </div>
  );
}
