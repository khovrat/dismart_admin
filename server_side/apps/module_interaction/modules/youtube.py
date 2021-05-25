import random
from youtubesearchpython import VideosSearch

from server_side.apps.module_interaction.modules.constants import SEARCH_ENGINE, LIMIT


def get_text():
    texts = [get_video(language) for language in SEARCH_ENGINE.keys()]
    return texts[random.randint(0, len(SEARCH_ENGINE) - 1)]


def get_video(language):
    videos = VideosSearch(SEARCH_ENGINE[language], limit=LIMIT).result()["result"]
    video = videos[random.randint(0, len(SEARCH_ENGINE) - 1)]
    return video["link"]
