from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot


@processor(state_manager, from_states='', message_types=message_types.Text, update_types=update_types.Message)
def say_hello(bot, update, state):
    text = update.get_message().get_text()
    if text == 'Alireza':
        bot.sendMessage(update.get_chat().get_id(), "Hello Alireza!")
        state.name = 'got_their_name'
        state.save()
    else:
        bot.sendMessage(update.get_chat().get_id(), "Nah")
        state.name = 'failed_to_give_name'
        state.save()
