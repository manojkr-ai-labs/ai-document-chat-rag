"use client";

import { Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";

interface IndexButtonProps {
  onIndex: () => void;
  isLoading: boolean;
}

export default function IndexButton({
  onIndex,
  isLoading,
}: IndexButtonProps) {
  return (
    <Button
      className="w-full"
      onClick={onIndex}
      disabled={isLoading}
    >
      {isLoading ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Indexing Documents...
        </>
      ) : (
        "Index Documents"
      )}
    </Button>
  );
}