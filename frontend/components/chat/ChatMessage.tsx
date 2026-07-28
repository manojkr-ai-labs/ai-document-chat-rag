interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export default function ChatMessage({
  role,
  content,
}: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white border text-gray-900"
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">
          {content}
        </p>
      </div>
    </div>
  );
}