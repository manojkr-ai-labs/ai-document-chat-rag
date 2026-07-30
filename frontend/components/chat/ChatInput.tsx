"use client";

import { useState } from "react";
import { Send } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
   onSend: (question: string) => void;
   onStop: () => void;
   isLoading: boolean;
}

export default function ChatInput({
   onSend,
   onStop,
   isLoading,
}: ChatInputProps) {
  const [question, setQuestion] = useState("");

  const handleSubmit = () => {
    if (!question.trim()) return;

    onSend(question);

    setQuestion("");
  };

  return (
    <div className="flex gap-3">
      <Input
        placeholder="Ask a question about your documents..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSubmit();
          }
        }}
      />

      <Button
          onClick={isLoading ? onStop : handleSubmit}
        >
          {isLoading ? (
            <>
              <span className="text-lg">■</span>
              <span className="ml-2">Stop</span>
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              <span className="ml-2">Send</span>
            </>
          )}
        </Button>
    </div>
  );
}