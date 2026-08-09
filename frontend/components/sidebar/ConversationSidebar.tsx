"use client";

import NewChatButton from "./NewChatButton";
import ConversationItem from "./ConversationItem";

import { useConversations } from "@/hooks/useConversation";

interface ConversationSidebarProps {
  selectedConversationId?: string;
  onSelectConversation: (id: string) => void;
  onNewChatStarted?: () => void;
}

export default function ConversationSidebar({
  selectedConversationId,
  onSelectConversation,
  onNewChatStarted,
}: ConversationSidebarProps) {
  const { data, isLoading, isError } = useConversations();

  // API shape: { success, data: Conversation[] }
  const conversations = Array.isArray(data?.data)
    ? data.data
    : Array.isArray(data)
      ? data
      : [];

  const handleCreateConversation = () => {
    // Do not create an empty row in the DB — first message creates the chat
    onNewChatStarted?.();
  };
  const handleDeleteConversation = (id: string) => {
    // If the deleted conversation is currently selected,
    // clear the current chat.
    if (selectedConversationId === id) {
      onSelectConversation("");
    }

    // Refresh sidebar and backend state.
    window.location.reload();
  };
  return (
    <div className="flex h-full w-80 flex-col border-r bg-white p-4">
      <NewChatButton
        onCreate={handleCreateConversation}
        isLoading={false}
      />

      <div className="mt-4 flex-1 overflow-y-auto">
        {isLoading && (
          <p className="text-sm text-gray-500">
            Loading conversations...
          </p>
        )}

        {isError && (
          <p className="text-sm text-red-500">
            Failed to load chat history.
          </p>
        )}

        {!isLoading &&
          !isError &&
          conversations.length === 0 && (
            <p className="text-sm text-gray-500">
              No chat history yet. Ask a question to start.
            </p>
          )}

        {conversations.map((conversation: any) => {
          const id =
            conversation.id ??
            conversation.conversation_id;

          if (!id) return null;

          const title =
            conversation.title ||
            conversation.preview ||
            "New Chat";

          return (
            <ConversationItem
              key={id}
              id={id}
              title={title}
              selected={selectedConversationId === id}
              onClick={() => onSelectConversation(id)}
               onDelete={handleDeleteConversation}
            />
          );
        })}
      </div>
    </div>
  );
}
