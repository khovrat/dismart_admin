from decouple import config
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import ugettext as _
from server_side.apps.module_interaction.additional_modules.df_response_lib import *
from server_side.apps.module_interaction.additional_modules import articles, youtube, wiki


def send_welcome(language, base_language):
    translation.activate(language)
    fulfillmentText = _("Welcome_message_telegram")
    tg = telegram_response()
    buttons = [
        [_('Go_to_site'), 'https://dismart.herokuapp.com/'],
        [_('Change_language'), 'change_language'],
        [_('Start_conversation'), 'start_conversation']
    ]
    aog_sr = tg.card_response(fulfillmentText, buttons)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply


def send_consult(language, base_language):
    translation.activate(language)
    fulfillmentText = _('Go_to_expert: ') + config("MY_TELEGRAM")
    tg = telegram_response()
    aog_sr = tg.card_response(fulfillmentText, [])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply


def send_help(language, base_language):
    translation.activate(language)
    fulfillmentText = _('Bye')
    tg = telegram_response()
    aog_sr = tg.card_response(fulfillmentText, [])
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply



def send_wiki(language, base_language):
    fulfillmentText = wiki.get_text()
    return send_base(fulfillmentText, language, base_language)


def send_youtube(language, base_language):
    fulfillmentText = youtube.get_text()
    return send_base(fulfillmentText, language, base_language)


def send_article(language, base_language):
    fulfillmentText = articles.get_text()
    return send_base(fulfillmentText, language, base_language)


def send_base(fulfillmentText, language, base_language):
    translation.activate(language)
    tg = telegram_response()
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    buttons = [
        [_('Article'), 'article'],
        [_('Video'), 'video'],
        [_('Archive'), 'archive']
    ]
    aog_btn = tg.card_response(fulfillmentText, buttons)
    ff_messages = ff_response.fulfillment_messages([aog_btn])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply


def change_language(language, base_language):
    translation.activate(language)
    fulfillmentText = _("Change_language_message")
    tg = telegram_response()
    buttons = [
        ['English', 'en'], ['Deutsch', 'de'],
        ['Русский', 'ru'], ['Беларуская', 'be'],
        ['Українська', 'uk']
    ]
    aog_sr = tg.card_response(fulfillmentText, buttons)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply


def start_conversation(language, base_language):
    translation.activate(language)
    fulfillmentText = _("Start_conversation_message")
    tg = telegram_response()
    buttons = [
        [_('Article'), 'article'],
        [_('Video'), 'video'],
        [_('Archive'), 'archive']
    ]
    aog_sr = tg.card_response(fulfillmentText, buttons)
    ff_response = fulfillment_response()
    ff_text = ff_response.fulfillment_text(fulfillmentText)
    ff_messages = ff_response.fulfillment_messages([aog_sr])
    reply = ff_response.main_response(ff_text, ff_messages)
    translation.activate(base_language)
    return reply
