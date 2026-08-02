from typing import Optional
from sqlalchemy.orm import Session

from src.repositories.conversation_repository import ConversationRepository
from src.repositories.message_repository import MessageRepository
from src.models.conversation import Conversation


class ConversationService:

    def __init__(self, db: Session):
        self.db = db

        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

    def create_conversation(
    self,
    title: str = "New Chat",
  ) -> Conversation:
     """
     Create a new conversation.
     """

     return self.conversation_repo.create(title)

    def get_conversation(self, conversation_id: str)-> Optional[Conversation]:
        """
        Get a conversation by ID.
        """
    
        return self.conversation_repo.get(conversation_id) 
    
    def list_conversations(self) -> list[Conversation]:
     return self.conversation_repo.list_all()

    def delete_conversation(
    self,
    conversation_id: str,
) -> bool:

     """
    Delete a conversation.

    Returns:
        True if deleted.
        False if conversation does not exist.
    """

     conversation = self.get_conversation(conversation_id)

     if conversation is None:
        return False

     self.conversation_repo.delete(conversation)

     return True