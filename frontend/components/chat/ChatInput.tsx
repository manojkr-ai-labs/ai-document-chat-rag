"use client";

import { useRef, useState } from "react";
import { Send, Square } from "lucide-react";
import useAutoResizeTextarea from "@/hooks/useAutoResizeTextarea";
interface ChatInputProps {
  onSend: (message: string) => void;
  onStop: () => void;
  isStreaming: boolean;
}

export default function ChatInput({
  onSend,
  onStop,
  isStreaming,
}: ChatInputProps) {
  const [message, setMessage] = useState("");
    const {
      textareaRef,
      resizeTextarea,
      resetTextarea,
    } = useAutoResizeTextarea();
    
const handleChange = (
  e: React.ChangeEvent<HTMLTextAreaElement>
) => {
  setMessage(e.target.value);

  requestAnimationFrame(resizeTextarea);
};

  const handleSubmit = () => {
    const text = message.trim();

    if (!text) return;

    onSend(text);

    setMessage("");

    resetTextarea();
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      if (!isStreaming) {
        handleSubmit();
      }
    }
  };

  return ( 
    <div className="flex w-full items-end gap-3"> 
     <textarea
          ref={textareaRef}
          value={message}
          rows={1}
          placeholder="Ask a question about your documents..."
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={isStreaming}
          className="
            flex-1
            min-w-0
            w-full
            min-h-[48px]
            max-h-48
            resize-none
            overflow-y-auto
            rounded-xl
            border
            border-slate-300
            bg-white
            px-4
            py-3
            text-sm
            leading-6
            shadow-sm
            outline-none
            transition-all
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-500
            disabled:bg-slate-100
          "
        />
      {isStreaming ? (
        <button
          onClick={onStop}
          className="
            flex
            items-center
            gap-2
            rounded-xl
            bg-red-600
             shrink-0
            px-5
            py-3
            font-medium
            text-white
            transition
            hover:bg-red-700
          "
        >
          <Square size={18} />
          Stop
        </button>
      ) : (
        <button
          onClick={handleSubmit}
          disabled={!message.trim()}
          className="
            flex
             shrink-0
            items-center
            gap-2
            rounded-xl
            bg-blue-600
            px-5
            py-3
            font-medium
            text-white
            transition
            hover:bg-blue-700
            disabled:cursor-not-allowed
            disabled:opacity-50
          "
        >
          <Send size={18} />
          Send
        </button>
      )}
    </div>
  );
}