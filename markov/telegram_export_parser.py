import json
from io import StringIO

class TelegramExportParser:
    def __init__(self, filename: str, identifier: str=None):
        self.messages = []
        with open(filename, "r", encoding="utf-8") as fp:
            chat = json.load(fp)
        for message in chat["messages"]:
            if message.get("text") and isinstance(message["text"], str) and not message.get("forwarded_from"):
                if not identifier or identifier == message["from_id"]:
                    self.messages.extend([x.lower() for x in message["text"].split("\n") if x])

    def save(self, filename: str):
        with open(filename, "w", encoding="utf-8") as fp:
            for message in self.messages:
                print(message, file=fp)

if __name__ == "__main__":
    # володя user247122292
    # леха user321133849
    # игорь user424294329
    # жека user427163348
    export = TelegramExportParser(".input/result.json", identifier="user247122292")
    export.save(".input/result.txt")
