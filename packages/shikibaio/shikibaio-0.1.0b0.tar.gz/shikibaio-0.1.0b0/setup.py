# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shikibaio', 'shikibaio.adapt_clients', 'shikibaio.enums', 'shikibaio.types']

package_data = \
{'': ['*']}

install_requires = \
['aiocometd>=0.4.5,<0.5.0']

setup_kwargs = {
    'name': 'shikibaio',
    'version': '0.1.0b0',
    'description': 'Asynchronous bot development framework for shikimori.',
    'long_description': '<p align="center">\n  <a href="https://github.com/ren3104/shikibaio/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ren3104/shikibaio"></a>\n  <a href="https://pypi.org/project/shikibaio"><img src="https://img.shields.io/pypi/v/shikibaio?color=blue&logo=pypi&logoColor=FFE873" alt="PyPi package version"></a>\n  <a href="https://pypi.org/project/shikibaio"><img src="https://img.shields.io/pypi/pyversions/shikibaio.svg?logo=python&logoColor=FFE873" alt="Supported python versions"></a>\n  <img src="https://img.shields.io/github/repo-size/ren3104/shikibaio" alt="GitHub repo size">\n  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>\n</p>\n\n~~Shikimori bot asyncio~~ Shikibaio - это асинхронный python фреймворк разработки ботов для [shikimori](https://shikimori.one).\n\n- [Установка](#установка)\n- [Поддерживаемые клиенты](#поддерживаемые-клиенты)\n- [Пример эхо бота](#пример-эхо-бота)\n- [Зависимости](#зависимости)\n\n## Установка\n```bash\npip install -U shikibaio\n```\n\n## Поддерживаемые клиенты\n| Логотип | Название | Версии |\n| --- | --- | --- |\n| [<img src="https://raw.githubusercontent.com/SecondThundeR/shikithon/main/assets/logo.png" alt="shikithon" height="50">](https://github.com/SecondThundeR/shikithon) | [Shikithon](https://github.com/SecondThundeR/shikithon) | >=2.0.0 |\n| [<img src="https://raw.githubusercontent.com/ren3104/Shiki4py/main/assets/shiki4py_logo_v2.jpg" alt="shiki4py" height="50">](https://github.com/ren3104/Shiki4py) | [Shiki4py](https://github.com/ren3104/Shiki4py) | >=2.1.0 |\n\nЕсли вы разработчик и хотите добавить свой клиет в эту таблицу, то можете сделать это несколькими способами:\n1. Добавить [сюда](https://github.com/ren3104/shikibaio/tree/main/shikibaio/adapt_clients) файл с классом переопределившим методы класса [BaseAdapt](https://github.com/ren3104/shikibaio/blob/main/shikibaio/adapt_clients/base.py) и добавить себя в таблицу выше.\n2. Написать мне в shikimori ([тык](https://shikimori.one/Ren3104)), чтобы я помог с этим.\n\n## Пример эхо бота\nВ этом примере я буду использовать клиент shikithon, но вы можете использовать любой другой поддерживаемый клиент.\n```python\nfrom shikithon import ShikimoriAPI\nfrom shikibaio import Dispatcher\nfrom shikibaio.types import Event\n\n\n# Создаем клиент\n# Если ваш бот будет отвечать на комментарии, то нужно указать api ключи с доступом к comments ресурсу\n# (про это можно почитать подробнее в документации используемого вами клиента и https://shikimori.one/api/doc)\nclient = ShikimoriAPI()\n# Создаем диспетчер\ndp = Dispatcher(client)\n\n\n# Создаем функцию, которая будет получать новые комментарии и отвечать на них\n@dp.on_event()\nasync def echo(event: Event):\n    await event.answer(event.text)\n\n\n# Подписываемся на обновления топика профиля\ndp.subscribe_topic(topic_id=555400, is_user_topic=True)\n# Запускаем бота\ndp.run()\n```\n\n## Зависимости\n- [aiocometd](https://github.com/robertmrk/aiocometd) - для взаимодействия с faye сервером по веб сокету.\n',
    'author': 'ren3104',
    'author_email': '2ren3104@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ren3104/shikibaio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
