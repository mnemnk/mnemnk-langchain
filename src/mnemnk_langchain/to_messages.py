import json
import sys

from langchain_core.messages.base import messages_to_dict
from langchain_core.messages.utils import convert_to_messages


def main():
    # Ensure sys.stdin/stdout uses UTF-8 encoding
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

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
                [_kind, value] = parse_input(line)
                messages = convert_to_messages(value)
                out_value = messages_to_dict(messages)
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
