"use client";

interface ConversationItemProps {
  id: string;
  title: string;
  selected?: boolean;
  onClick: () => void;
}

export default function ConversationItem({
  id,
  title,
  selected = false,
  onClick,
}: ConversationItemProps) {
  return (
    <button
      key={id}
      onClick={onClick}
      className={`
        mb-2
        flex
        w-full
        items-center
        gap-2
        rounded-lg
        px-3
        py-2
        text-left
        transition-colors
        ${
          selected
            ? "bg-blue-100 text-blue-700"
            : "hover:bg-gray-100"
        }
      `}
    >
      <span>💬</span>

      <span className="truncate">
        {title}
      </span>
    </button>
  );
}