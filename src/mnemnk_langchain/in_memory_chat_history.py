import argparse
import json
import sys

from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import messages_from_dict, trim_messages

from . import parse_input, write_out


CONFIG = {
    "max_messages": 7,
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
    
    history = []

    # Main loop
    for line in sys.stdin:
        line = line.strip()

        if line.startswith(".CONFIG "):
            [_, config_str] = line.split(" ", 1)
            config.update(json.loads(config_str))
            continue

        if line == ".QUIT":
            break

        if line.startswith(".IN "):
            try:
                [kind, value] = parse_input(line)

                # Add the new message to the history
                if kind == "message":
                    messages = messages_from_dict([value])
                    history.append(messages[0])
                elif kind == "messages":
                    messages = messages_from_dict(value)
                    history.extend(messages)
                else:
                    print(f"Error: Unknown kind: {kind}", file=sys.stderr)
                    continue
                
                # Trim the history to the max count
                trimed = trim_messages(
                    history,
                    # Keep the last <= n_count tokens of the messages.
                    strategy="last",
                    token_counter=len,
                    # When token_counter=len, each message
                    # will be counted as a single token.
                    # Remember to adjust for your use case
                    max_tokens=config["max_messages"],
                    # Most chat models expect that chat history starts with either:
                    # (1) a HumanMessage or
                    # (2) a SystemMessage followed by a HumanMessage
                    start_on="human",
                    # Most chat models expect that chat history ends with either:
                    # (1) a HumanMessage or
                    # (2) a ToolMessage
                    # end_on=("human", "tool"),
                    # Usually, we want to keep the SystemMessage
                    # if it's present in the original history.
                    # The SystemMessage has special instructions for the model.
                    include_system=True,
                )
                history = trimed
                if not history:
                    continue

                out_value = messages_to_dict(history)
                write_out("messages", out_value)
            
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
            
            continue
