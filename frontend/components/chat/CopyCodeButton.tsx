"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";

interface CopyCodeButtonProps {
  code: string;
}

export default function CopyCodeButton({
  code,
}: CopyCodeButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="absolute right-3 top-3 z-10 rounded-md bg-slate-700 p-2 text-white transition hover:bg-slate-600"
      title="Copy code"
    >
      {copied ? (
        <Check className="h-4 w-4 text-green-400" />
      ) : (
        <Copy className="h-4 w-4" />
      )}
    </button>
  );
}