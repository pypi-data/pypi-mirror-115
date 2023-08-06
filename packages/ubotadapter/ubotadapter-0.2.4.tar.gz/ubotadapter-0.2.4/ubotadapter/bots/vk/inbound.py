from ubotadapter import InboundMessage

from .user import VKUser


class VKInboundMessage(InboundMessage):
    _UserClass = VKUser

    @property
    def object(self):
        return self['object']

    @property
    def message(self):
        return self.object['message']

    @property
    def group_id(self) -> int:
        return self.get('group_id', None)

    @property
    def text(self) -> str:
        return self.message['text']

    @property
    def user_id(self) -> str:
        return self.message['from_id']

    @property
    def user_id_url(self) -> str:
        return f'@id{self.user_id}'

    @property
    def chat_id(self) -> str:
        return self.message['peer_id']

    @property
    def message_id(self) -> str:
        return self.message['id']

    @property
    def secret_code(self) -> str:
        return self.get('secret', None)
