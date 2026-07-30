import { ReactNode } from "react";
import clsx from "clsx";

interface MessageBubbleProps {
  role: "user" | "assistant";
  children: ReactNode;
}

export default function MessageBubble({
  role,
  children,
}: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div
      className={clsx(
        " group w-fit max-w-[90%] rounded-2xl px-4 py-3 shadow-sm",
        isUser
          ? "ml-auto bg-blue-600 text-white"
          : "mr-auto border bg-white text-slate-900"
      )}
    >
      {children}
    </div>
  );
}