from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union, Type

from .botcontext import BotContext
from .botmsg import BotMessage
from .user import User


class InboundMessage(ABC):
    __slots__ = ('_data',)

    _UserClass = User

    def __init__(self, data):
        self._data = data
        self.validate()
        self._user = self._UserClass(self.user_id)

    def __getitem__(self, key):
        return self._data[key]

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    # region User
    @property
    def user(self) -> User:
        return self._user

    @property
    @abstractmethod
    def user_id(self) -> Union[int, str]:
        pass

    @property
    @abstractmethod
    def user_id_url(self) -> str:
        pass

    @property
    def user_visual_name(self) -> str:
        return self.user.visual_name or self.user.short_name

    @property
    def user_data(self):
        return None

    # endregion

    @property
    @abstractmethod
    def chat_id(self) -> Union[int, str]:
        pass

    @property
    @abstractmethod
    def message_id(self) -> Union[int, str]:
        pass

    @property
    def is_private(self) -> bool:
        return self.user_id == self.chat_id

    def get(self, key, default_value):
        return self._data.get(key, default_value)

    @property
    @abstractmethod
    def secret_code(self) -> str:
        pass

    def validate(self):
        assert self.user_id is not None


class InboundProcessor(ABC):
    error_message_default = 'Inbound processing error'

    @staticmethod
    @abstractmethod
    def process(context: BotContext, inbound: InboundMessage):
        """context.replies.add(BotMessage(inbound.text))"""
        pass


class DefaultInboundProcessor(InboundProcessor):
    """Empty processor"""

    @staticmethod
    def process(context: BotContext, inbound: InboundMessage):
        pass


class EchoInboundProcessor(InboundProcessor):
    """Echo processor"""

    @staticmethod
    def process(context: BotContext, inbound: InboundMessage):
        context.replies.add(BotMessage(inbound.text))


class EchoReplyToInboundProcessor(InboundProcessor):
    """Echo processor"""

    @staticmethod
    def process(context: BotContext, inbound: InboundMessage):
        context.replies.add(BotMessage(inbound.text, is_reply_to_message=True))


class EchoNameInboundProcessor(InboundProcessor):
    """Echo processor"""

    @staticmethod
    def process(context: BotContext, inbound: InboundMessage):
        # text = f'{context.bot.get_user_visual_name(inbound)} is your name.'
        text = f'{inbound.user.visual_name} is your name.'
        context.replies.add(BotMessage(text))


class InboundMessageFactory:
    __slots__ = ('_default_inbound_message_class',)

    def __init__(self, default_inbound_message_class: Type[InboundMessage]):
        self._default_inbound_message_class = default_inbound_message_class

    def create(self, data) -> InboundMessage:
        inbound_message_class = self.get_inbound_message_class(data)
        return inbound_message_class(data)

    def get_inbound_message_class(self, data) -> Type[InboundMessage]:
        return self._default_inbound_message_class
