import json
from typing import Any


def parse_input(line: str):
    [_cmd, kind, value] = line.split(" ", 2)
    value = json.loads(value)
    return kind, value


def write_out(kind: str, value: Any):
    json_value = json.dumps(value)
    print(f".OUT {kind} {json_value}", flush=True)
