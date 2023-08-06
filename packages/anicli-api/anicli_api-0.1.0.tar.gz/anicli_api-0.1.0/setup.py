# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anicli_api', 'anicli_api.extractors']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'anicli-api',
    'version': '0.1.0',
    'description': 'Anime extractor api implementation',
    'long_description': '# anicli-api\n\nПрограммный интерфейс парсера аниме с различных источников.\n\nПрисутствует поддержка sync и async методов с помощью `httpx`,для получения информации и прямых ссылок на видео.\n# Overview\nМодуль экстрактора имеют следующую структуру пошагового получения объекта:\n```shell\n# Extractor works schema:\n    [Extractor]\n        | search(<query>)/ongoing()  -> List[SearchResult | Ongoing]\n        V                           \n  [SearchResult | Ongoing]          \n         | get_anime()  -> AnimeInfo\n         V                          \n    [AnimeInfo]                     \n        | get_episodes()  -> List[Episode]  \n        V                           \n    [Episode]                      \n        | get_videos()  -> List[Video]              \n        V                           \n    [Video]\n        | get_source()  -> Dict or Str\n        V\n    {quality: url, ...} or url\n```\n\n# Quickstart example\nСмотрите примеры в [examples](examples)\n\n# Примечание\n\nЕсли вы будете этот проект использовать в **production** условиях, особенно в высоко нагруженных решениях, \nто выстаивайте архитектуру своих проектов **на предварительном сборе информации** \n(например, полученные данные сохранять в базу данных и только из неё возвращать), \nтак как большинство парсеров работает в обход официальных методов и применяются такие библиотеки как re, bs4. \nПоэтому могут быть проблемы от производительности, до получения ошибок по типу 403 (срабатывание ddos защиты) или \n502 (доступа к сайту запрещён).\n\n**Этот проект не включает инструменты кеширования и сохранения всех полученных данных, только эндпоинты**\n\n# DEV\n [DEV](DEV.MD)\n\n# Contributing\n[CONTRIBUTING](CONTRIBUTING.MD)\n\n# TODO\n* ~~CI CD автотестов~~\n* Получение видео по ссылке (like yt-dlp)\n* ~~asyncio tests~~\n* ~~coverage~~\n* ~~добавить примеры~~\n* ~~Написать документацию для high level применения~~ пока на уровне example примеров\n* ~~Написать документацию для low level разработки экстракторов~~\n* ~~Дописать asyncio методы для animego~~\n* Портировать anilibria, animevost, animania экстракторы из старого проекта\n',
    'author': 'Georgiy aka Vypivshiy',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
