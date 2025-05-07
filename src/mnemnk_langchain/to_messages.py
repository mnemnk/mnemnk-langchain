from typing import override

from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages

from . import AgentContext, AgentData, BaseAgent, run_agent


class ToMessagesAgent(BaseAgent):
    """Convert string input to messages."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        messages = convert_to_messages(data.value)
        self.write_out(ctx, "message", AgentData("message", messages_to_dict(messages)))


def main():
    run_agent(ToMessagesAgent)


if __name__ == "__main__":
    main()
