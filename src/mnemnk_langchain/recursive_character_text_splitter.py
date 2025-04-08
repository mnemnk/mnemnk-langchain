import argparse
import json
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import parse_input, write_out


CONFIG = {
    "chunk_size": 4000,
    "chunk_overlap": 20,
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
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-3.5-turbo",
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
    )

    # Main loop
    for line in sys.stdin:
        line = line.strip()

        if line.startswith(".CONFIG "):
            try:
                [_, config_str] = line.split(" ", 1)
                config.update(json.loads(config_str))
                text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    model_name="gpt-3.5-turbo",
                    chunk_size=config["chunk_size"],
                    chunk_overlap=config["chunk_overlap"],
                )
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

            continue

        if line == ".QUIT":
            break

        if line.startswith(".IN "):
            try:
                [_ch, _kind, value] = parse_input(line)

                texts = text_splitter.split_text(value)
                for text in texts:
                    write_out("texts", "text", text)

            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
            
            continue
