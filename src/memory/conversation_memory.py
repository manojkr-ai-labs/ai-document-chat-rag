class ConversationMemory:

    def __init__(self):
        self.messages = []

    def add_user(self, message):
        self.messages.append(("User", message))

    def add_ai(self, message):
        self.messages.append(("AI", message))

    def get_context(self):
        return "\n".join(
            f"{role}: {text}"
            for role, text in self.messages
        )

    def clear(self):
        self.messages.clear()
# Singleton instance
memory = ConversationMemory()        