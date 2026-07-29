import { Loader2 } from "lucide-react";

export default function ThinkingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="flex items-center gap-2 rounded-2xl border bg-white px-4 py-3 shadow-sm">
        <Loader2 className="h-4 w-4 animate-spin text-blue-600" />

        <span className="text-sm text-gray-600">
          AI is thinking...
        </span>
      </div>
    </div>
  );
}