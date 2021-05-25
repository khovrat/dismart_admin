import wikipedia
import random
from wikipedia.exceptions import DisambiguationError, PageError

from server_side.apps.module_interaction.modules.constants import LIMIT, SEARCH_ENGINE


def get_text():
    language = random.choice(list(SEARCH_ENGINE.keys()))
    texts = get_article(language)
    return texts


def get_article(language):
    wikipedia.set_lang(language)
    titles = wikipedia.search(SEARCH_ENGINE[language], LIMIT)
    try:
        page = wikipedia.page(titles[random.randint(0, LIMIT - 1)])
    except (DisambiguationError, PageError) as e:
        page = get_article(language)
    return page.url
