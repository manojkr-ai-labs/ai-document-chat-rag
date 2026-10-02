import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import CopyCodeButton from "./CopyCodeButton";
import CitationList from "./CitationList";
import type { Citation } from "@/types/chat";

interface MarkdownRendererProps {
  content: string;
  citations?: Citation[];
}

export default function MarkdownRenderer({
  content,
  citations,
}: MarkdownRendererProps) {
  return (
    <>
      <div className="prose prose-sm max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              const code = String(children).replace(/\n$/, "");

            if (match) {
                  return (
                    <div className="relative">
                      <CopyCodeButton code={code} />

                      <SyntaxHighlighter
                        style={oneDark}
                        language={match[1]}
                        PreTag="div"
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
      </div>

      <CitationList citations={citations} />
    </>
  );
}