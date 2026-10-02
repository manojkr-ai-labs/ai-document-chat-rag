"use client";

interface NewChatButtonProps {
  onCreate: () => void;
  isLoading?: boolean;
}

export default function NewChatButton({
  onCreate,
  isLoading = false,
}: NewChatButtonProps) {
  return (
    <button
      onClick={onCreate}
      disabled={isLoading}
      className="
        mb-4
        w-full
        rounded-lg
        bg-blue-600
        px-4
        py-2
        font-medium
        text-white
        transition
        hover:bg-blue-700
        disabled:cursor-not-allowed
        disabled:bg-blue-400
      "
    >
      {isLoading ? "Creating..." : "+ New Chat"}
    </button>
  );
}