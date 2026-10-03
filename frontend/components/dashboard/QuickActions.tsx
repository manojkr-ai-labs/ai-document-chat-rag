"use client";

import {
  Upload,
  Database,
  MessageSquare,
  HeartPulse,
} from "lucide-react";
import { useRouter } from "next/navigation";

import QuickAction from "./QuickAction";

export default function QuickActions() {
  const router = useRouter();

  const handleUpload = () => {
    router.push("/upload");
  };

  const handleIndex = () => {
    router.push("/documents");
  };

  const handleChat = () => {
    router.push("/chat");
  };

  const handleHealth = () => {
    router.push("/health");
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">
        Quick Actions
      </h2>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <QuickAction
          title="Upload PDF"
          description="Upload PDF documents"
          icon={<Upload className="h-8 w-8" />}
          buttonText="Upload"
          onClick={handleUpload}
        />

        <QuickAction
          title="Index Documents"
          description="Create vector embeddings"
          icon={<Database className="h-8 w-8" />}
          buttonText="Index"
          onClick={handleIndex}
        />

        <QuickAction
          title="Start Chat"
          description="Ask questions to your documents"
          icon={<MessageSquare className="h-8 w-8" />}
          buttonText="Chat"
          onClick={handleChat}
        />

        <QuickAction
          title="Health Check"
          description="Verify backend status"
          icon={<HeartPulse className="h-8 w-8" />}
          buttonText="Check"
          onClick={handleHealth}
        />
      </div>
    </div>
  );
}