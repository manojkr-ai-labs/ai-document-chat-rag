import type { Citation } from "@/types/chat";

import MarkdownRenderer from "./MarkdownRenderer";
import StreamingMessage from "./StreamingMessage";
import MessageTimestamp from "./MessageTimestamp";
import MessageBubble from "./MessageBubble";
import MessageActions from "./MessageActions";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  citations?: Citation[];
  isStreaming?: boolean;
}

export default function ChatMessage({
  role,
  content,
  timestamp,
  citations,
  isStreaming = false,
}: ChatMessageProps) {
  const isUser = role === "user";

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content);
  };

  const handleRegenerate = () => {
    console.log("Regenerate clicked");
  };

  const handleLike = () => {
    console.log("Like clicked");
  };

  const handleDislike = () => {
    console.log("Dislike clicked");
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <MessageBubble role={role}>
        {isStreaming ? (
          <StreamingMessage content={content} />
        ) : (
          <MarkdownRenderer
            content={content}
            citations={citations}
          />
        )}

        {!isStreaming && (
          <MessageTimestamp timestamp={timestamp} />
        )}

        {!isStreaming && role === "assistant" && (
          <MessageActions
            onCopy={handleCopy}
            onRegenerate={handleRegenerate}
            onLike={handleLike}
            onDislike={handleDislike}
          />
        )}
      </MessageBubble>
    </div>
  );
}