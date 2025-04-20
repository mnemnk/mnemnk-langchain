from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages, messages_from_dict, trim_messages

from . import BaseAgent, run_agent


class InMemoryChatHistory(BaseAgent):
    """In-memory chat history agent."""

    DEFAULT_CONFIG = {
        "max_messages": 7,
        "start_on": None,
        "include_system": False,
    }

    def __init__(self, config=None):
        """Initialize the InMemoryChatHistory with configuration."""
        super().__init__(config)
        self.history = []

    def process_input(self, ch: str, kind: str, value: any):
        if ch == "reset":
            self.history = []
            return

        if kind != "message":
            return

        # Add the new message to the history
        if isinstance(value, list):
            messages = messages_from_dict(value)
        else:
            messages = messages_from_dict([value])

        self.history.extend(messages)
        
        # Trim the history to the max count
        self.history = trim_messages(
            self.history,
            # Keep the last <= n_count tokens of the messages.
            strategy="last",
            token_counter=len,
            # When token_counter=len, each message
            # will be counted as a single token.
            # Remember to adjust for your use case
            max_tokens=self.config["max_messages"],
            # Most chat models expect that chat history starts with either:
            # (1) a HumanMessage or
            # (2) a SystemMessage followed by a HumanMessage
            start_on=self.config["start_on"],
            # Most chat models expect that chat history ends with either:
            # (1) a HumanMessage or
            # (2) a ToolMessage
            # end_on=("human", "tool"),
            # Usually, we want to keep the SystemMessage
            # if it's present in the original history.
            # The SystemMessage has special instructions for the model.
            include_system=self.config["include_system"],
        )
        if not self.history:
            return

        out_value = messages_to_dict(self.history)
        self.write_out("message", "message", out_value)


def main():
    run_agent(InMemoryChatHistory)


if __name__ == "__main__":
    main()
