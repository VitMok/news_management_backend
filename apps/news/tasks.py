from news_management_backend.celery import app
from .services import (
    _get_links_to_news_from_yandex,
    _get_links_to_news_from_ozon,
    _parsing_news_yandex,
    _parsing_news_ozon,
)


@app.task
def parsing_news_from_yandex(amount_news):
    """ Парсинг новостей с яндекса """
    links_yandex_news = _get_links_to_news_from_yandex(amount_news)
    _parsing_news_yandex(links_yandex_news)

@app.task
def parsing_news_from_ozon(amount_news):
    """ Парсинг новостей с озона """
    links_ozon_news, dates = _get_links_to_news_from_ozon(amount_news)
    _parsing_news_ozon(links_ozon_news, dates)