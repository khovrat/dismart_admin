import json
from django.views.decorators.csrf import csrf_exempt

from server_side import settings
from server_side.apps.data_interaction import crud
from server_side.apps.module_interaction.bot_commands import *

from server_side.apps.shared_logic import utils


@csrf_exempt
def webhook(request):
    request_t = json.loads(request.body)
    text = utils.get_string('text', request_t['originalDetectIntentRequest']['payload']['data'])
    text_q = utils.get_string('queryText', request_t['queryResult'])
    reply = '{}'
    if text == '/start':
        crud.create_telegram_user(
            user=request_t['originalDetectIntentRequest']['payload']['data']['from']['id'],
            language=request_t['originalDetectIntentRequest']['payload']['data']['from']['language_code']
        )
        reply = send_welcome(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text == '/consult':
        reply = send_consult(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text == '/help':
        reply = send_help(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q == 'change_language':
        reply = change_language(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q in ('en', 'de', 'ru', 'be', 'uk'):
        crud.update_telegram_user(
            user=request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id'],
            language=text_q
        )
        reply = send_welcome(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q == 'start_conversation':
        reply = start_conversation(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q == 'archive':
        reply = send_wiki(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q == 'video':
        reply = send_youtube(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    if text_q == 'article':
        reply = send_article(
            language=crud.read_telegram_user_user(
                request_t['originalDetectIntentRequest']['payload']['data']['callback_query']['from']['id']
            ).language,
            base_language=settings.LANGUAGE_CODE
        )
    return JsonResponse(reply, safe=False)
