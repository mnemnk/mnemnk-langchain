from langchain_core.messages.human import HumanMessage
from langchain_core.messages.base import message_to_dict

from . import BaseAgent, run_agent


class ToHumanMessageAgent(BaseAgent):
    """Convert string input to HumanMessage."""

    def process_input(self, _ch: str, _kind: str, value: any):
        message = HumanMessage(content=value)
        out_value = message_to_dict(message)
        self.write_out("message", "message", out_value)


def main():
    run_agent(ToHumanMessageAgent)


if __name__ == "__main__":
    main()
