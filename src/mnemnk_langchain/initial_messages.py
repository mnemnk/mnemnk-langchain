import argparse
import json
import sys

from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages


CONFIG = {
    "messages": None,
}


def main():
    # Ensure sys.stdin/stdout uses UTF-8 encoding
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    is_initial = True

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config json string")
    args = parser.parse_args()

    # Load config from command line arguments or use default
    config = CONFIG.copy()
    if args.config:
        config.update(json.loads(args.config))
    
    # Main loop
    for line in sys.stdin:
        line = line.strip()

        if line.startswith(".CONFIG "):
            # do nothing
            continue

        if line == ".QUIT":
            break

        if line.startswith(".IN "):
            try:
                [kind, value] = parse_input(line)

                if kind == "reset":
                    is_initial = True
                    continue

                messages = []

                if is_initial:
                    initial_messages = config["messages"]
                    if initial_messages:
                        messages = messages_to_dict(convert_to_messages(initial_messages))
                    is_initial = False
                
                if kind == "message":
                    messages.append(value)
                elif kind == "messages":
                    messages.extend(value)
                else:
                    print(f"Error: Unknown kind: {kind}", file=sys.stderr)
                    continue

                write_out("messages", messages)
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
