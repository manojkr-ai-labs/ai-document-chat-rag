"use client";

import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import ChatHistory, {
  type Message,
} from "@/components/chat/ChatHistory";
import ConversationSidebar from "@/components/sidebar/ConversationSidebar";
import ChatInput from "@/components/chat/ChatInput";
import ThinkingIndicator from "@/components/chat/ThinkingIndicator";

import { useConversation } from "@/hooks/useConversation";
import { streamChat } from "@/services/chatStream";

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
    useState<string | undefined>();

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const abortControllerRef =
    useRef<AbortController | null>(null);

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

  // ==========================================================
  // Load conversation history
  // ==========================================================

  useEffect(() => {
    if (!selectedConversationId) {
      setMessages([]);
      return;
    }

    // Do not overwrite streamed messages
    if (isStreaming) {
      return;
    }

    if (isConversationPending) {
      setMessages([]);
      return;
    }

    if (isConversationError) {
      setMessages([]);
      return;
    }

    const body = conversationResponse as any;

    // Support:
    // { data: { messages } }
    // and
    // { messages }

    const rawMessages =
      body?.data?.messages ??
      body?.messages ??
      null;

    if (rawMessages == null) {
      return;
    }

    const requestId = ++loadRequestIdRef.current;

    const nextMessages = mapMessages(rawMessages);

    if (requestId === loadRequestIdRef.current) {
      setMessages(nextMessages);
    }
  }, [
    selectedConversationId,
    conversationResponse,
    isConversationPending,
    isConversationError,
    isStreaming,
  ]);

  // ==========================================================
  // Auto scroll
  // ==========================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // ==========================================================
  // Select conversation
  // ==========================================================

  const handleSelectConversation = (id: string) => {
    if (id === selectedConversationId) {
      return;
    }

    setMessages([]);
    setSelectedConversationId(id);
  };

  // ==========================================================
  // New conversation
  // ==========================================================

  const handleNewChatStarted = () => {
    setMessages([]);
    setSelectedConversationId(undefined);
  };

  // ==========================================================
  // Send message + stream response
  // ==========================================================

  const handleSend = async (question: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
      timestamp: new Date(),
    };

    const assistantId = crypto.randomUUID();

    // Create AbortController for this request
    const controller = new AbortController();

    abortControllerRef.current = controller;

    // --------------------------------------------------------
    // Immediately show user message + empty assistant message
    // --------------------------------------------------------

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
      // ------------------------------------------------------
      // Start streaming
      // ------------------------------------------------------

      const conversationId = await streamChat(
        question,
        selectedConversationId ?? null,

        // ----------------------------------------------------
        // Called for EVERY streamed chunk
        // ----------------------------------------------------

        (chunk) => {
          console.log("PAGE RECEIVED CHUNK:", JSON.stringify(chunk));

          setMessages((prev) =>
            prev.map((message) =>
              message.id === assistantId
                ? {
                    ...message,
                    content:
                      message.content + chunk,
                  }
                : message
            )
          );
        },

        controller.signal
      );

      // ------------------------------------------------------
      // Validate conversation ID
      // ------------------------------------------------------

      if (!conversationId) {
        throw new Error(
          "No conversation_id returned from stream"
        );
      }

      // ------------------------------------------------------
      // Select newly created conversation
      // ------------------------------------------------------

      setSelectedConversationId(conversationId);

      // ------------------------------------------------------
      // Refresh conversation from backend
      // ------------------------------------------------------

      await queryClient.invalidateQueries({
        queryKey: ["conversation", conversationId],
      });

      await queryClient.invalidateQueries({
        queryKey: ["conversations"],
      });
    } catch (error) {
      // ------------------------------------------------------
      // User stopped streaming
      // ------------------------------------------------------

      if (
        error instanceof DOMException &&
        error.name === "AbortError"
      ) {
        console.log("Streaming stopped by user.");

        return;
      }

      // ------------------------------------------------------
      // Streaming failed
      // ------------------------------------------------------

      console.error("Streaming error:", error);

      setMessages((prev) => [
        ...prev.filter(
          (message) => message.id !== assistantId
        ),
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "❌ Sorry, I couldn't generate an answer.\nPlease try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      abortControllerRef.current = null;
      setIsStreaming(false);
    }
  };

  // ==========================================================
  // Stop streaming
  // ==========================================================

  const handleStop = () => {
    abortControllerRef.current?.abort();
  };

  // ==========================================================
  // UI
  // ==========================================================
return (
  <div className="flex h-full min-h-0">
    {/* Conversation Sidebar */}
    <ConversationSidebar
      selectedConversationId={selectedConversationId}
      onSelectConversation={handleSelectConversation}
      onNewChatStarted={handleNewChatStarted}
    />

    {/* Main Chat */}
    <div className="flex min-w-0 min-h-0 flex-1 flex-col">
      <div className="mx-auto flex h-full min-h-0 w-full max-w-5xl flex-col gap-6 p-6">

        {/* Header */}
        <div className="shrink-0">
          <h1 className="text-3xl font-bold">
            AI Document Chat
          </h1>

          <p className="mt-2 text-gray-500">
            Ask questions about your indexed PDF documents.
          </p>
        </div>

        {/* Messages */}
        <div className="min-h-0 flex-1 overflow-y-auto rounded-xl border bg-slate-50 p-6">
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

        {/* Thinking */}
        {isStreaming && (
          <div className="shrink-0">
            <ThinkingIndicator />
          </div>
        )}

        {/* Input */}
        <div className="shrink-0">
          <ChatInput
            onSend={handleSend}
            onStop={handleStop}
            isStreaming={isStreaming}
            disabled={isLoadingConversation}
          />
        </div>

      </div>
    </div>
  </div>
);
}