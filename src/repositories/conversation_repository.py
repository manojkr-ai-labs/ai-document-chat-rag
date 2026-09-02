from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.models.conversation import Conversation
from src.repositories.message_repository import MessageRepository


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        title: str = "New Chat",
    ) -> Conversation:
        """
        Create a new conversation.
        """
        conversation = Conversation(title=title)

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get(
        self,
        conversation_id: str,
    ) -> Optional[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )

    def list_all(self) -> list[Conversation]:
        return (
            self.db.query(Conversation)
            .order_by(
                Conversation.updated_at.desc()
            )
            .all()
        )

    def delete(
        self,
        conversation: Conversation,
    ) -> None:
        self.db.delete(conversation)
        self.db.commit()

    def rename(
        self,
        conversation: Conversation,
        new_title: str,
    ) -> Conversation:
        conversation.title = new_title
        conversation.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(conversation)

        return conversation