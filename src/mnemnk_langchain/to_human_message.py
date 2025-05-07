from typing import override

from langchain_core.messages.base import message_to_dict
from langchain_core.messages.human import HumanMessage

from . import AgentContext, AgentData, BaseAgent, run_agent


class ToHumanMessageAgent(BaseAgent):
    """Convert string input to HumanMessage."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        if isinstance(data.value, list):
            messages = [
                message_to_dict(HumanMessage(content=item)) for item in data.value
            ]
            self.write_out(ctx, "message", AgentData("message", messages))
            return

        message = HumanMessage(content=data.value)
        self.write_out(ctx, "message", AgentData("message", message_to_dict(message)))


def main():
    run_agent(ToHumanMessageAgent)


if __name__ == "__main__":
    main()
