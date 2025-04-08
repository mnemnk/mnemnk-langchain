import sys

from langchain_community.document_loaders import WebBaseLoader

from . import parse_input, write_out


def main():
    # Ensure sys.stdin/stdout uses UTF-8 encoding
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    # Main loop
    for line in sys.stdin:
        line = line.strip()

        if line.startswith(".CONFIG "):
            continue

        if line == ".QUIT":
            break

        if line.startswith(".IN "):
            try:
                [_ch, _kind, value] = parse_input(line)

                if value.startswith("http://") or value.startswith("https://"):
                    loader = WebBaseLoader(web_path=value)
                    documents = loader.load()
                    if not documents:
                        print("Error: No documents found", file=sys.stderr)
                        continue
                    document = documents[0]

                    doc_dict = {
                        "metadata": document.metadata,
                        "page_content": document.page_content,
                    }
                    write_out("document", "document", doc_dict)
                    write_out("content", "text", document.page_content)

            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

            continue
