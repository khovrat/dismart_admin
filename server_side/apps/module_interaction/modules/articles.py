import random
from server_side.apps.data_interaction import crud


def get_text():
    texts = get_article()
    if len(texts) == 0:
        return ''
    return texts[random.randint(0, len(texts) - 1)]


def get_article():
    articles = crud.read_article()
    articles_links = []
    if articles.count() == 0:
        return []
    for article in articles:
        articles_links.append(article.text)
    return articles_links
