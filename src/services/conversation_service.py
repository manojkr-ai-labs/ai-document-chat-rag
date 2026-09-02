from typing import Any, Optional

from sqlalchemy.orm import Session

from src.models.conversation import Conversation
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.message_repository import MessageRepository


PLACEHOLDER_TITLES = {"New Chat", "string", ""}


def title_from_question(question: str, max_len: int = 60) -> str:
    cleaned = " ".join(question.strip().split())

    if not cleaned:
        return "New Chat"

    if len(cleaned) > max_len:
        return f"{cleaned[: max_len - 1]}…"

    return cleaned


class ConversationService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    def create_conversation(
        self,
        title: str = "New Chat",
    ) -> dict[str, Any]:
        conversation = self.conversation_repo.create(title)

        return self._serialize_conversation(
            conversation,
            messages=[],
        )

    def get_conversation(
        self,
        conversation_id: str,
    ) -> Optional[Conversation]:
        return self.conversation_repo.get(conversation_id)

    def list_conversations(self) -> list[dict[str, Any]]:
        """
        Return conversations as plain dictionaries for the sidebar.

        Uses the first user message as the display title when the
        stored title is still a placeholder.
        """
        conversations = self.conversation_repo.list_all()
        result: list[dict[str, Any]] = []

        for conversation in conversations:
            messages = self.message_repo.list_by_conversation(
                conversation.id
            )

            # Skip empty chats so the sidebar only shows real history.
            if not messages:
                continue

            result.append(
                self._serialize_conversation(
                    conversation,
                    messages=messages,
                )
            )

        return result

    def get_conversation_with_messages(
        self,
        conversation_id: str,
    ) -> Optional[dict[str, Any]]:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            return None

        messages = self.message_repo.list_by_conversation(
            conversation_id
        )

        return self._serialize_conversation(
            conversation,
            messages=messages,
            include_messages=True,
        )

    def rename_conversation(
        self,
        conversation_id: str,
        title: str,
    ) -> Optional[dict[str, Any]]:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            return None

        updated = self.conversation_repo.rename(
            conversation,
            title,
        )

        messages = self.message_repo.list_by_conversation(
            conversation_id
        )

        return self._serialize_conversation(
            updated,
            messages=messages,
        )

    def delete_conversation(self, conversation_id: str) -> bool:
        conversation = self.get_conversation(conversation_id)

        if conversation is None:
            return False

        self.conversation_repo.delete(conversation)

        return True

    def _serialize_conversation(
        self,
        conversation: Conversation,
        messages: list,
        include_messages: bool = False,
    ) -> dict[str, Any]:
        first_user = next(
            (message for message in messages if message.role == "user"),
            None,
        )

        preview = first_user.content if first_user else None

        title = conversation.title or "New Chat"

        if title in PLACEHOLDER_TITLES and preview:
            title = title_from_question(preview)

        payload: dict[str, Any] = {
            "id": conversation.id,
            "title": title,
            "preview": preview,
            "message_count": len(messages),
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }

        if include_messages:
            payload["messages"] = [
                {
                    "id": message.id,
                    "role": message.role,
                    "content": message.content,
                    "citations": message.citations,
                    "created_at": message.created_at,
                }
                for message in messages
            ]

        return payload