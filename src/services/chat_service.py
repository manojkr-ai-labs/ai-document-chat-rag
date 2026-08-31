from sqlalchemy.orm import Session

from src.models.message import Message
from src.repositories.conversation_repository import ConversationRepository
from src.repositories.message_repository import MessageRepository
from src.services.conversation_service import (
    PLACEHOLDER_TITLES,
    title_from_question,
)
from src.services.rag_service import answer_question


class ChatService:
    """
    Service responsible for handling chat workflow.
    """

    def __init__(self, db: Session):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    def chat(
        self,
        question: str,
        conversation_id: str | None = None,
    ):
        print("========== CHAT SERVICE ==========")
        print(question)

        if conversation_id is None:
            conversation = self.conversation_repo.create(
                title_from_question(question)
            )
        else:
            conversation = self.conversation_repo.get(
                conversation_id
            )

            if conversation is None:
                raise ValueError("Conversation not found")

            # Rename placeholder titles after the first real question
            if conversation.title in PLACEHOLDER_TITLES:
                conversation = self.conversation_repo.rename(
                    conversation,
                    title_from_question(question),
                )

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=question,
            citations=None,
        )
        self.message_repo.save(user_message)
        messages = self.message_repo.list_by_conversation(
            conversation.id
        )
        conversation_history = "\n".join(
            f"{message.role.capitalize()}: {message.content}"
            for message in messages
        )
        result = answer_question(question, conversation=conversation_history)

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["answer"],
            citations=result["citations"],
        )
        self.message_repo.save(assistant_message)

        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "answer": result["answer"],
            "citations": result["citations"],
        }
