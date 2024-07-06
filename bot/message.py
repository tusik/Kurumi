from enum import Enum

from botpy.message import Message, GroupMessage


class MessageType(Enum):
    Channel = 1
    Group = 2


class KurumiMessage:
    def __init__(self, message_id, content):
        self.media_type = 1
        self.member = None
        self.author = None
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

    def set_image(self,image):
        self.file = image
        self.media_type = 2
    @classmethod
    def create(cls, channel_msg: Message = None, group_msg: GroupMessage = None):
        c = None
        if channel_msg is not None:
            c = cls.create_channel_message(message_id=channel_msg.id, channel_id=channel_msg.channel_id)
            c.member = channel_msg.member
            c.author = channel_msg.author
        elif group_msg is not None:
            c = cls.create_group_message(message_id=group_msg.id, group_id=group_msg.group_openid)
            c.author = group_msg.author
        return c
    @classmethod
    def create_channel_message(cls, message_id, channel_id, content=None):
        message = cls(message_id, content)
        message.set_channel_id(channel_id)
        return message

    @classmethod
    def create_group_message(cls, message_id, group_id, content=None):
        message = cls(message_id, content)
        message.set_group_id(group_id)
        return message
