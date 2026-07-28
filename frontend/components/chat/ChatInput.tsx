"use client";

import { useState } from "react";
import { Send } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
  onSend: (question: string) => void;
  isLoading: boolean;
}

export default function ChatInput({
  onSend,
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
        onClick={handleSubmit}
        disabled={isLoading}
      >
        <Send className="h-4 w-4" />

        <span className="ml-2">
          {isLoading ? "Thinking..." : "Send"}
        </span>
      </Button>
    </div>
  );
}