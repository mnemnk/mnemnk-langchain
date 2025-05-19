from langchain_core.messages.utils import convert_to_messages, messages_from_dict

from . import AgentData


def data_to_messages(data: AgentData):
    if data.kind == "messages":
        # TODO: Check if the input value is a list of messages
        return messages_from_dict(data.value)

    elif data.kind == "message":
        if isinstance(data.value, list):
            messages = []
            for item in data.value:
                messages.append(messages_from_dict([item]))
            return messages

        messages = messages_from_dict([data.value])
        return messages[0]

    else:
        if isinstance(data.value, list):
            return convert_to_messages(data.value)
        else:
            messages = convert_to_messages([data.value])
            return messages[0]
