import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import type { Citation } from "@/types/chat";
import CitationList from "./CitationList";
import CopyCodeButton from "./CopyCodeButton";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  citations?: Citation[];
}

export default function ChatMessage({
  role,
  content,
  timestamp,
  citations,
}: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${
          isUser
            ? "bg-blue-600 text-white"
            : "border bg-white text-gray-900"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap text-sm">{content}</p>
        ) : (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  const code = String(children).replace(/\n$/, "");

                  if (!inline && match) {
                    return (
                      <div className="relative">
                        <CopyCodeButton code={code} />

                        <SyntaxHighlighter
                          style={oneDark}
                          language={match[1]}
                          PreTag="div"
                          {...props}
                        >
                          {code}
                        </SyntaxHighlighter>
                      </div>
                    );
                  }

                  return (
                    <code
                      className="rounded bg-slate-200 px-1 py-0.5"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
              }}
            >
              {content}
            </ReactMarkdown>

            <CitationList citations={citations} />
          </div>
        )}

        <p
          className={`mt-2 text-xs ${
            isUser ? "text-blue-100" : "text-gray-500"
          }`}
        >
          {timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}