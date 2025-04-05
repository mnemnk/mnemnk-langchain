import argparse
import json
import sys

from langchain.chat_models import init_chat_model
from langchain_core.messages.base import message_to_dict
from langchain_core.messages.utils import messages_from_dict


CONFIG = {
    "model": "gemma3:4b",
    "model_provider": "ollama",
}


def main():
    # Ensure sys.stdin/stdout uses UTF-8 encoding
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config json string")
    args = parser.parse_args()

    # Load config from command line arguments or use default
    config = CONFIG.copy()
    if args.config:
        config.update(json.loads(args.config))
    
    # Initialize the chat model
    model = init_chat_model(config["model"], model_provider=config["model_provider"])

    # Main loop
    for line in sys.stdin:
        line = line.strip()

        if line.startswith(".CONFIG "):
            [_, config_str] = line.split(" ", 1)
            config.update(json.loads(config_str))
            model = init_chat_model(config["model"], model_provider=config["model_provider"])
            continue

        if line == ".QUIT":
            break

        if line.startswith(".IN "):
            [kind, value] = parse_input(line)
            if kind == "message":
                messages = messages_from_dict([value])
                resp = model.invoke(messages)

            elif kind == "messages":
                messages = messages_from_dict(value)
                resp = model.invoke(messages)
            else:
                resp = model.invoke(value)

            out_value = message_to_dict(resp)
            write_out("ai_message", out_value)
            continue


def parse_input(line: str):
    [_cmd, kind, value] = line.split(" ", 2)
    value = json.loads(value)
    return kind, value


def write_out(kind: str, value: any):
    json_value = json.dumps(value)
    print(f".OUT {kind} {json_value}", flush=True)
