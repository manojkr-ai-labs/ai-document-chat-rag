from collections.abc import Generator

from sqlalchemy.orm import Session

from src.models.message import Message
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.message_repository import MessageRepository
from src.services.conversation_service import (
    PLACEHOLDER_TITLES,
    title_from_question,
)
from src.services.rag_stream_service import stream_answer


class ChatStreamService:
    """
    Service responsible for streaming chat responses
    and persisting conversation messages.
    """

    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    def get_or_create_conversation_id(
        self,
        question: str,
        conversation_id: str | None = None,
    ) -> str:
        """
        Get an existing conversation or create a new one.
        """

        if conversation_id is None:
            conversation = self.conversation_repo.create(
                title_from_question(question)
            )

            return conversation.id

        conversation = self.conversation_repo.get(
            conversation_id
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        return conversation.id

    def stream(
        self,
        question: str,
        conversation_id: str,
    ) -> Generator[str, None, None]:
        """
        Stream the RAG response and persist messages.
        """

        conversation = self.conversation_repo.get(
            conversation_id
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        # Rename placeholder conversation title
        if conversation.title in PLACEHOLDER_TITLES:
            conversation = self.conversation_repo.rename(
                conversation,
                title_from_question(question),
            )

        # --------------------------------------------------
        # Save user message
        # --------------------------------------------------

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=question,
            citations=None,
        )

        self.message_repo.save(user_message)

        # --------------------------------------------------
        # Stream assistant response
        # --------------------------------------------------

        complete_answer = ""

        for chunk in stream_answer(question):
            complete_answer += chunk

            yield chunk

        # --------------------------------------------------
        # Save final assistant message
        # --------------------------------------------------

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=complete_answer,
            citations=None,
        )

        self.message_repo.save(assistant_message)