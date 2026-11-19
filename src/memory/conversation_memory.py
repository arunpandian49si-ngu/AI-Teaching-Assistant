
class ConversationMemory:

    def __init__(self, max_history=10):
        self.max_history = max_history
        self.sessions = {}

    def add_message(self, session_id, role, content):

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

        # Keep only the latest messages
        self.sessions[session_id] = (
            self.sessions[session_id][-self.max_history:]
        )

    def get_history(self, session_id):
        return self.sessions.get(session_id, [])

    def clear_history(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def format_history(self, session_id):

        history = self.get_history(session_id)
        formatted_history = []

        for message in history:
            role = message["role"].capitalize()
            content = message["content"]

            formatted_history.append(
                f"{role}: {content}"
            )

        return "\n".join(formatted_history)
