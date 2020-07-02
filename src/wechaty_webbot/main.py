import logging
import os
import asyncio
from typing import Optional
from aiohttp import web
import threading

from chatie_grpc.wechaty import FriendshipType

from wechaty_webbot.server import puppetware_start_server
from wechaty_puppet import ScanStatus

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    Friendship)

logging.basicConfig(level=logging.WARN)


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_HOSTIE_TOKEN in the environment variables.
    #
    if 'WECHATY_PUPPET_HOSTIE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_HOSTIE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Java Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_hostie_token
        ''')

    global bot

    bot = Wechaty()
    from wechaty_plugin_contrib import DingDongPlugin
    bot.use(DingDongPlugin())

    # def on_friendship(fs):
    #     print(fs)

    # bot.on('friendship', on_friendship)
    # app.add_routes([web.get('/', say_hello)])

    await asyncio.gather(
        puppetware_start_server(bot),
        bot.start()
    )
    # await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
