import unittest

from ubotadapter.botmsg import Keyboard
from ubotadapter.inbound import *
from .test_tools import *


class TestKeyboardInboundProcessor(InboundProcessor):
    @staticmethod
    def process(context: BotContext, inbound: InboundMessage):
        buttons = [['button_1', 'button_2'], ['button_3']]
        context.replies.add(
            BotMessage('Choose:', keyboard=Keyboard(buttons=buttons, one_time=True, in_line=True)))
        context.replies.add(
            BotMessage('Choose!', keyboard=Keyboard(buttons=buttons, one_time=True, in_line=False)))


class TestBotsInboundProcessor(unittest.TestCase):
    def test_tg_inbound_processor(self):
        bot = get_tg_bot()
        bot.set_inbound_processor(EchoInboundProcessor)

        result = bot.handle(TGTestMessage().get_message())
        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

        result = bot.handle(TGCallbackTestMessage().get_message())
        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

    def test_vk_inbound_processor(self):
        bot = get_vk_bot()
        bot.set_inbound_processor(EchoInboundProcessor)
        result = bot.handle(VKTestMessage().get_message(bot.config.bot_id))
        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

    def test_dtf_inbound_processor(self):
        bot = get_dtf_bot()
        bot.set_inbound_processor(EchoInboundProcessor)
        result = bot.handle(DTFTestMessage().get_message())
        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

    def test_vk_get_name(self):
        bot = get_vk_bot()
        bot.set_inbound_processor(EchoNameInboundProcessor)
        message = VKTestMessage().get_message(bot.config.bot_id)
        result = bot.handle(message)
        self.assertTrue(bot.context.replies.count == 1)
        self.assertTrue(result.is_ok, msg=result.report())

    def test_tg_keyboard_inbound_processor(self):
        bot = get_tg_bot()
        bot.set_inbound_processor(TestKeyboardInboundProcessor)

        result = bot.handle(TGTestMessage().get_message())

        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

    def test_vk_keyboard_inbound_processor(self):
        bot = get_vk_bot()
        bot.set_inbound_processor(TestKeyboardInboundProcessor)

        result = bot.handle(VKTestMessage().get_message(bot.config.bot_id))

        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)

    def test_dtf_keyboard_inbound_processor(self):
        bot = get_dtf_bot()
        bot.set_inbound_processor(TestKeyboardInboundProcessor)

        result = bot.handle(DTFTestMessage().get_message())

        self.assertTrue(result.is_ok, msg=result.report())
        self.assertFalse(result.no_replies)


if __name__ == '__main__':
    import logging

    logger = logging.getLogger('ubotadapter')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    unittest.main()
