import json
from typing import Any


def parse_input(line: str) -> tuple[str, str, Any]:
    [_cmd, ch, kind, value] = line.split(" ", 3)
    value = json.loads(value)
    return ch, kind, value


def write_out(ch: str, kind: str, value: Any):
    json_value = json.dumps(value)
    print(f".OUT {ch} {kind} {json_value}", flush=True)
