import ChatMessage from "./ChatMessage";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface ChatHistoryProps {
  messages: Message[];
}

export default function ChatHistory({
  messages,
}: ChatHistoryProps) {
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

  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          role={message.role}
          content={message.content}
        />
      ))}
    </div>
  );
}