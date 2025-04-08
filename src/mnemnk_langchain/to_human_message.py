import sys

from langchain_core.messages.human import HumanMessage
from langchain_core.messages.base import message_to_dict

from . import parse_input, write_out


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
                [_ch, _kind, value] = parse_input(line)
                message = HumanMessage(content=value)
                out_value = message_to_dict(message)
                write_out("message", "message", out_value)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

            continue
