import argparse
import json
import sys

from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import messages_from_dict, trim_messages


CONFIG = {
    "max_messages": 5,
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
    
    hisotry = []

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
                    hisotry.append(messages[0])
                elif kind == "messages":
                    messages = messages_from_dict(value)
                    hisotry.extend(messages)
                else:
                    print(f"Error: Unknown kind: {kind}", file=sys.stderr)
                    continue
                
                # Trim the history to the max count
                trimed = trim_messages(
                    hisotry,
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
                hisotry = trimed
                if not hisotry:
                    continue

                out_value = messages_to_dict(hisotry)
                write_out("messages", out_value)
            
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
            
            continue


def parse_input(line: str):
    [_cmd, kind, value] = line.split(" ", 2)
    value = json.loads(value)
    return kind, value


def write_out(kind: str, value: any):
    json_value = json.dumps(value)
    print(f".OUT {kind} {json_value}", flush=True)
