from enum import Enum


class MessageType(Enum):
    Channel = 1
    Group = 2


class KurumiMessage:
    def __init__(self, message_id, content):
        self.member = None
        self.message_type = None
        self.channel_id = None
        self.group_id = None
        self.file = None
        self.content = content
        self.message_id = message_id

    def set_channel_id(self, channel_id):
        self.message_type = MessageType.Channel
        self.channel_id = channel_id

    def set_group_id(self, group_id):
        self.message_type = MessageType.Group
        self.group_id = group_id

    @classmethod
    def create_channel_message(cls, message_id, channel_id, content = None):
        message = cls(message_id, content)
        message.set_channel_id(channel_id)
        return message

    @classmethod
    def create_group_message(cls, message_id, group_id, content = None):
        message = cls(message_id, content)
        message.set_group_id(group_id)
        return message
