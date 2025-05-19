from typing import Any, Optional, override

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages.base import message_to_dict

from . import AgentContext, AgentData, BaseAgent, run_agent
from .utils import data_to_messages

load_dotenv()


class ChatModelAgent(BaseAgent):
    """Chat model agent that interacts with a chat model."""

    DEFAULT_CONFIG = {
        "model": "gemma3:4b",
        "model_provider": "ollama",
        "kwargs": {},
    }

    def __init__(self, config=None):
        """Initialize the ChatModelAgent with configuration."""
        super().__init__(config)
        self.process_config(self.config)

    @override
    def process_config(self, _new_config: Optional[dict[str, Any]]):
        # Initialize the chat model
        self.model = init_chat_model(
            self.config["model"],
            model_provider=self.config["model_provider"],
            configurable_fields="any",
            **self.config["kwargs"],
        )

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        messages = data_to_messages(data)

        if data.kind == "messages":
            # Skip if the last message is not from human to avoid infinite loop
            if messages and messages[-1].type != "human":
                return

            # Invoke the model and get the response
            resp = self.model.invoke(messages)
            self.write_out(ctx, "message", AgentData("message", message_to_dict(resp)))

        elif data.kind == "message":
            if isinstance(data.value, list):
                out_messages = []
                for msgs in messages:
                    if msgs and msgs[-1].type != "human":
                        continue
                    # Invoke the model and get the response
                    resp = self.model.invoke(msgs)
                    out_value = message_to_dict(resp)
                    out_messages.append(out_value)
                self.write_out(ctx, "message", AgentData("message", out_messages))
                return

            # Invoke the model and get the response
            resp = self.model.invoke(messages)
            self.write_out(ctx, "message", AgentData("message", message_to_dict(resp)))

        else:
            if isinstance(messages, list):
                # Skip if the last message is not from human to avoid infinite loop
                if messages and messages[-1].type != "human":
                    return

                # Invoke the model and get the response
                resp = self.model.invoke(messages)
                self.write_out(
                    ctx, "message", AgentData("message", message_to_dict(resp))
                )
                return

            if messages.type != "human":
                return

            # Invoke the model and get the response
            resp = self.model.invoke([messages])
            self.write_out(ctx, "message", AgentData("message", message_to_dict(resp)))


def main():
    run_agent(ChatModelAgent)


if __name__ == "__main__":
    main()
