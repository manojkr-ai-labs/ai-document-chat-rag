"use client";

import { useState } from "react";
import { renameConversation,deleteConversation } from "@/services/conversation";

interface ConversationItemProps {
  id: string;
  title: string;
  selected?: boolean;
  onClick: () => void;
   onDelete?: (id: string) => void;
}

export default function ConversationItem({
  id,
  title,
  selected = false,
  onClick,
  onDelete
}: ConversationItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const [isSaving, setIsSaving] = useState(false);

 const [isDeleting, setIsDeleting] = useState(false);

  const handleRename = async () => {
    const newTitle = editTitle.trim();

    if (!newTitle || newTitle === title) {
      setEditTitle(title);
      setIsEditing(false);
      return;
    }

    try {
      setIsSaving(true);

      await renameConversation(id, newTitle);

      setIsEditing(false);

      // Refresh the page so useConversations()
      // gets the latest title from backend.
      window.location.reload();
    } catch (error) {
      console.error("Failed to rename conversation:", error);
      setEditTitle(title);
    } finally {
      setIsSaving(false);
    }
  };
   const handleDelete = async () => {
    const confirmed = window.confirm(
      `Delete "${title}"?\n\nThis will permanently delete the conversation and its messages.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setIsDeleting(true);

      await deleteConversation(id);

      onDelete?.(id);
    } catch (error) {
      console.error(
        "Failed to delete conversation:",
        error
      );

      window.alert(
        "Failed to delete conversation. Please try again."
      );
    } finally {
      setIsDeleting(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleRename();
    }

    if (event.key === "Escape") {
      setEditTitle(title);
      setIsEditing(false);
    }
  };

  if (isEditing) {
    return (
      <div className="mb-2 flex w-full items-center gap-2">
        <input
          autoFocus
          value={editTitle}
          disabled={isSaving}
          onChange={(event) => setEditTitle(event.target.value)}
          onKeyDown={handleKeyDown}
          className="min-w-0 flex-1 rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-500"
        />

        <button
          type="button"
          disabled={isSaving}
          onClick={handleRename}
          className="rounded px-2 py-1 text-sm hover:bg-gray-100 disabled:opacity-50"
        >
          ✓
        </button>

        <button
          type="button"
          disabled={isSaving}
          onClick={() => {
            setEditTitle(title);
            setIsEditing(false);
          }}
          className="rounded px-2 py-1 text-sm hover:bg-gray-100 disabled:opacity-50"
        >
          ✕
        </button>
      </div>
    );
  }

  return (
    <div
      className={`mb-2 flex w-full items-center gap-1 rounded-lg transition-colors ${
        selected
          ? "bg-blue-100 text-blue-700"
          : "hover:bg-gray-100"
      }`}
    >
      <button
        type="button"
        onClick={onClick}
        className="flex min-w-0 flex-1 items-center gap-2 px-3 py-2 text-left"
        disabled={isDeleting}
      >
        <span>💬</span>

        <span className="truncate">
          {title}
        </span>
      </button>

      <button
        type="button"
        title="Rename conversation"
        onClick={(event) => {
          event.stopPropagation();
          setEditTitle(title);
          setIsEditing(true);
        }}
        disabled={isDeleting}
        className="mr-2 rounded px-2 py-1 text-sm hover:bg-white"
      >
        ✏️
      </button>
      <button
        type="button"
        title="Delete conversation"
        disabled={isDeleting}
        onClick={(event) => {
          event.stopPropagation();
          handleDelete();
        }}
        className="mr-2 rounded px-2 py-1 text-sm hover:bg-red-50 disabled:opacity-50"
      >
        {isDeleting ? "..." : "🗑️"}
      </button>
    </div>
  );
}