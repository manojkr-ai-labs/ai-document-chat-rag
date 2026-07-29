import type { Citation } from "@/types/chat";
import { FileText } from "lucide-react";

interface CitationListProps {
  citations?: Citation[];
}

export default function CitationList({
  citations = [],
}: CitationListProps) {
  if (!citations.length) return null;

  

  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs font-semibold text-gray-500">
        Sources
      </p> 
      {citations.map((citation, index) => (
        
        <div
          key={index}
          className="flex items-center gap-3 rounded-lg border bg-gray-50 p-3"
        >
          <FileText className="h-4 w-4 text-blue-600" />

          <div className="flex flex-col">
            <span className="text-sm font-medium">
              {citation.source.split(/[\\/]/).pop() || citation.source}
            </span>

            <span className="text-xs text-gray-500">
              Page {citation.page}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}