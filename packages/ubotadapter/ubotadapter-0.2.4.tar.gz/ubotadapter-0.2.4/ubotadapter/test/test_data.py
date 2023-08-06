import json
import os
import random

# from ubotadapter.test.test_tools import *

# Test data JSON fields #
# %bot%:
#   bot_message_receiver:
# bot_default_message:
from abc import ABC, abstractmethod

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(_CUR_DIR, 'data')

with open(os.path.join(DATA_DIR, 'testdata.json'), 'r', encoding='utf-8') as f:
    _TEST_DATA = json.load(f)


def get_random_default_message():
    return f'{_TEST_DATA["bot_default_message"]} [{random.randint(100, 100000)}]'


class TestMessage(ABC):
    @property
    def default_text(self) -> str:
        return f'{_TEST_DATA["bot_default_message"]} [{random.randint(100, 100000)}]'

    def get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        user_id = user_id or self.default_user_id
        text = text or self.default_text
        chat_id = chat_id or user_id
        return self._get_message(user_id=user_id, text=text, chat_id=chat_id, **kwargs)

    @abstractmethod
    def _get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        """Channel dependent message"""
        pass

    @property
    @abstractmethod
    def default_user_id(self) -> int:
        pass


class VKTestMessage(TestMessage):
    @property
    def default_user_id(self) -> int:
        return _TEST_DATA['vk']['bot_message_receiver']

    def _get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        return {
            'type': 'message_new',
            'object': {
                'message': {
                    'date': 1624210000,
                    'from_id': user_id,
                    'id': 1,
                    'out': 0,
                    'peer_id': chat_id,
                    'text': text,
                    'conversation_message_id': 600,
                    'fwd_messages': [],
                    'important': False,
                    'random_id': 0,
                    'attachments': [],
                    'is_hidden': False
                },
                'client_info': {
                    'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback',
                                       'intent_subscribe',
                                       'intent_unsubscribe'],
                    'keyboard': True,
                    'inline_keyboard': True,
                    'carousel': True,
                    'lang_id': 0
                }
            },
            'group_id': bot_id,
            'event_id': 'b6ca7d45d8055838911ed53a23f46b8098fe526f'
        }


class TGTestMessage(TestMessage):
    @property
    def default_user_id(self) -> int:
        return _TEST_DATA['telegram']['bot_message_receiver']

    def _get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        return {
            'update_id': 350516797,
            'message': {
                'message_id': 1,
                'from': {
                    'id': user_id,
                    'is_bot': False,
                    'first_name': 'Igor',
                    'last_name': 'Shephard',
                    'username': 'smyek',
                    'language_code': 'en'
                },
                'chat': {
                    'id': chat_id,
                    'first_name': 'Igor',
                    'last_name': 'Shephard',
                    'username': 'smyek',
                    'type': 'private'
                },
                'date': 1624210000,
                'text': text
            }
        }


class TGCallbackTestMessage(TestMessage):
    @property
    def default_user_id(self) -> int:
        return _TEST_DATA['telegram']['bot_message_receiver']

    def _get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        text = text or 'callback_test'
        return {
            'update_id': 350517096,
            'callback_query': {
                'id': '161535137947598551',
                'from': {
                    'id': user_id,
                    'is_bot': False,
                    'first_name': 'Igor',
                    'last_name': 'Shephard',
                    'username': 'smyek',
                    'language_code': 'en'
                },
                'message': {
                    'message_id': 581,
                    'from': {
                        'id': 1090207860,
                        'is_bot': True,
                        'first_name': 'STestBot',
                        'username': 'SmyekTestBot'
                    },
                    'chat': {
                        'id': -470399541, #chat_id,
                        'first_name': 'Igor',
                        'last_name': 'Shephard',
                        'username': 'smyek',
                        'type': 'private'
                    },
                    'date': 1627246822,
                    'text': 'Выбери',
                    'reply_markup': {
                        'inline_keyboard': [[{
                            'text': 'callback_test_button',
                            'callback_data': 'callback_test'
                        }
                        ]]
                    }
                },
                'chat_instance': '-4910036551047067769',
                'data': text
            }
        }


class DTFTestMessage(TestMessage):
    @property
    def default_user_id(self) -> int:
        return _TEST_DATA['dtf']['bot_message_receiver']

    def _get_message(self, user_id: int = None, text: str = None, chat_id: int = None, bot_id: int = None, **kwargs):
        text = text or get_random_default_message()
        test_entry_id = chat_id or 777326
        test_subsite_id = 130721
        reply_to = kwargs.get('reply_to', None)
        test_comment_id = kwargs.get('test_comment_id', 11825814)
        message = {
            "id": test_comment_id,
            "url": f'https://dtf.ru/{test_entry_id}?comment={11825814}',
            "text": text,
            "media": [

            ],
            "creator": {
                "id": user_id,
                "avatar": "https://leonardo.osnova.io/d49d71ab-f78a-db1d-b4c4-0c72b8fcda0e/",
                "name": "Igor Shephard",
                "url": f'https://dtf.ru/u/{user_id}'
            },
            "content": {
                "id": test_entry_id,
                "title": "test",
                "url": f'https://dtf.ru/apitest/{test_entry_id}',
                "owner": {
                    "id": test_subsite_id,
                    "name": "Полигон",
                    "avatar": "",
                    "url": ""
                }
            },
            "reply_to": None
        }
        if reply_to:
            message['reply_to'] = {
                "id": reply_to,
                "url": "https://",
                "text": "Это родительский комментарий",
                "media": [

                ],
                "creator": {
                    "id": 1,
                    "avatar": "https://",
                    "name": "TestUser",
                    "url": ""
                }
            }
        return message
