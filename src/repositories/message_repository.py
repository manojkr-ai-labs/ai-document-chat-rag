 
from sqlalchemy.orm import Session

from src.models.message import Message


class MessageRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
    self,
    message: Message,
) -> Message:
     """
     Save a message.
     """

     self.db.add(message)
     self.db.commit()
     self.db.refresh(message)

     return message    

    def list_by_conversation(
    self,
    conversation_id: str,
    ) -> list[Message]:

     """
    Return all messages for a conversation.
    """

     return (
        self.db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    def delete_by_conversation(self, conversation_id: str) -> None:

      """
      Delete all messages for a conversation.
      """
      (
        self.db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .delete(synchronize_session=False)
      )

      self.db.commit()