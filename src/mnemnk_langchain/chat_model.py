from typing import Optional
from langchain.chat_models import init_chat_model
from langchain_core.messages.base import message_to_dict
from langchain_core.messages.utils import convert_to_messages, messages_from_dict

from . import BaseAgent, run_agent

from dotenv import load_dotenv
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
    
    def process_config(self, _new_config: Optional[dict[str, any]]):
        # Initialize the chat model
        self.model = init_chat_model(
            self.config["model"],
            model_provider=self.config["model_provider"],
            configurable_fields="any",
            **self.config["kwargs"],
        )

    def process_input(self, _ch: str, kind: str, value: any):
        if kind == "message":
            if isinstance(value, list):
                messages = messages_from_dict(value)
            else:
                messages = messages_from_dict([value])
        else:
            messages = convert_to_messages(value)

        # Skip if the last message is from AI to avoid infinite loop
        if messages and messages[-1].type == "ai":
            return

        # Invoke the model and get the response
        resp = self.model.invoke(messages)
        out_value = message_to_dict(resp)
        self.write_out("message", "message", out_value)


def main():
    run_agent(ChatModelAgent)


if __name__ == "__main__":
    main()
