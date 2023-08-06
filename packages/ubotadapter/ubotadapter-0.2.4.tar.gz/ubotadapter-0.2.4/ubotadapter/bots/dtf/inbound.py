from functools import cached_property

from deteefapi import WebhookComment, DeteefAPI
from deteefapi.webhook import CommentCreator

from ubotadapter import InboundMessage
from .user import DTFUser


class DTFInboundMessage(InboundMessage):
    _UserClass = DTFUser

    @property
    def user_id(self) -> int:
        return self._comment.creator.id

    @property
    def user_id_url(self) -> str:
        return DeteefAPI.get_user_url(user_id=self.user_id, name=self._comment.creator.name)

    @property
    def chat_id(self) -> int:
        return self._comment.content.id

    @property
    def message_id(self) -> int:
        return self._comment.id

    @property
    def secret_code(self) -> str:
        # TODO: implement
        return ''

    @property
    def text(self) -> str:
        return self._comment.text

    @cached_property
    def _comment(self) -> WebhookComment:
        return WebhookComment(self._data)

    @property
    def user_data(self) -> CommentCreator:
        return self._comment.creator
