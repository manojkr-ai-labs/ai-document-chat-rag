import ChatMessage from "./ChatMessage";
import { Citation } from "@/types/chat";
 
export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  citations?: Citation[];
}

interface ChatHistoryProps {
  messages: Message[];
  isStreaming: boolean;
  isLoading?: boolean;
}

export default function ChatHistory({
  messages,
  isStreaming,
  isLoading = false,
}: ChatHistoryProps) {
  if (isLoading) {
    return (
      <div className="rounded-xl border border-dashed p-10 text-center text-gray-500">
        <h3 className="text-lg font-semibold">
          Loading conversation...
        </h3>

        <p className="mt-2 text-sm">
          Please wait while we load this chat.
        </p>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="rounded-xl border border-dashed p-10 text-center text-gray-500">
        <h3 className="text-lg font-semibold">
          No conversation yet
        </h3>

        <p className="mt-2 text-sm">
          Upload and index a PDF, then ask your first
          question.
        </p>
      </div>
    );
  }
  const lastAssistantIndex = messages
  .map((m) => m.role)
  .lastIndexOf("assistant");

  return (
    <div className="space-y-4">
      {messages.map((message, index) => (
      <ChatMessage
        key={message.id}
        role={message.role}
        content={message.content}
        timestamp={message.timestamp}
        citations={message.citations}
         isStreaming={
              isStreaming &&
              index === lastAssistantIndex &&
              message.role === "assistant"
            }
        />
      ))}
    </div>
  );
}