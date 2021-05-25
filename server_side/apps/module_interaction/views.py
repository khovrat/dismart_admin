import json
from django.views.decorators.csrf import csrf_exempt

from server_side import settings
from server_side.apps.module_interaction.bot_commands import *
from django.utils.translation import get_language

from server_side.apps.shared_logic import utils

USER_LANGUAGE = 'en'

@csrf_exempt
def webhook(request):
    global USER_LANGUAGE
    request_t = json.loads(request.body)
    text = utils.get_string('text', request_t['originalDetectIntentRequest']['payload']['data'])
    text_q = utils.get_string('queryText', request_t['queryResult'])
    if text == '/start':
        settings.LANGUAGE_CODE = request_t['originalDetectIntentRequest']['payload']['data']['from']['language_code']
    reply = '{}'
    if text == '/start':
        reply = send_welcome(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text == '/consult':
        reply = send_consult(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text == '/help':
        reply = send_help(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q == 'change_language':
        reply = change_language(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q in ('en', 'de', 'ru', 'be', 'uk'):
        settings.LANGUAGE_CODE = text_q
        reply = send_welcome(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q == 'start_conversation':
        reply = start_conversation(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q == 'archive':
        reply = send_wiki(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q == 'video':
        reply = send_youtube(settings.LANGUAGE_CODE, USER_LANGUAGE)
    if text_q == 'article':
        reply = send_article(settings.LANGUAGE_CODE, USER_LANGUAGE)
    return JsonResponse(reply, safe=False)
