from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages

from . import BaseAgent, run_agent


class ToMessagesAgent(BaseAgent):
    """Convert string input to messages."""

    def process_input(self, _ch: str, _kind: str, value: any):
        messages = convert_to_messages(value)
        out_value = messages_to_dict(messages)
        self.write_out("messages", "message", out_value)


def main():
    run_agent(ToMessagesAgent)


if __name__ == "__main__":
    main()
