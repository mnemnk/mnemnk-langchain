from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages

from . import BaseAgent, run_agent


class InitialMessagesAgent(BaseAgent):
    """Agent that handles initial messages and resets."""

    DEFAULT_CONFIG = {
        "messages": None,
    }

    def __init__(self, config=None):
        """Initialize the InitialMessagesAgent with configuration."""
        super().__init__(config)
        self.is_initial = False

    def process_input(self, ch: str, kind: str, value: any):
        if ch == "reset":
            self.is_initial = True
            return

        messages = []

        if self.is_initial:
            initial_messages = self.config["messages"]
            if initial_messages:
                messages = messages_to_dict(convert_to_messages(initial_messages))
            self.is_initial = False
        
        if isinstance(value, list):
            messages.extend(value)
        else:
            messages.append(value)

        self.write_out("messages", "message", messages)


def main():
    run_agent(InitialMessagesAgent)


if __name__ == "__main__":
    main()
