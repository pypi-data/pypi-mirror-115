from typing import Type

from ubotadapter import InboundMessage, InboundMessageFactory
from .user import TelegramUser


class TGInboundMessage(InboundMessage):
    _UserClass = TelegramUser

    @property
    def message(self):
        return self['message']

    @property
    def user_data(self) -> dict:
        return self._from

    @property
    def _from(self) -> dict:
        return self.message['from']

    @property
    def text(self) -> str:
        return self.message['text']

    @property
    def user_id(self) -> int:
        return self._from['id']

    @property
    def user_id_url(self) -> str:
        return f'@{self._from["username"]}'

    @property
    def chat_id(self) -> str:
        return self.message['chat']['id']

    @property
    def message_id(self) -> str:
        return self.message['message_id']

    @property
    def secret_code(self) -> None:
        return None

    @property
    def is_private(self) -> bool:
        return self.message('type', None) == 'private'


class TGInboundCallbackQuery(TGInboundMessage):
    @property
    def callback_query(self):
        return self['callback_query']

    @property
    def message(self):
        return self.callback_query['message']

    @property
    def _from(self):
        return self.callback_query['from']

    @property
    def text(self) -> str:
        data = self.callback_query['data']
        if isinstance(data, str):
            return data
        return ''


class TGInboundMessageFactory(InboundMessageFactory):
    def get_inbound_message_class(self, data) -> Type[InboundMessage]:
        if 'callback_query' in data:
            return TGInboundCallbackQuery
        return self._default_inbound_message_class
