from aiohttp import web
from wechaty import Wechaty
from wechaty_puppet import ContactQueryFilter

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    Friendship)

routes = web.RouteTableDef()

context = dict()


def bot_view_wrapper(view_func):
    """
    A decorator which automatically add bot and path match as params into the view function.
    Extends the pure aiohttp way.
    :param view_func:
    :return:
    """

    async def _view(request: web.Request):
        return await view_func(
            request,
            bot=context.get('bot'),
            **dict(request.match_info)
        )

    return _view


@routes.get(r'/contact/find_all')
@bot_view_wrapper
async def view(request: web.Request, bot: Wechaty):
    contacts: [Contact] = await bot.Contact.find_all()
    data = [contact.payload.to_dict() for contact in contacts]
    return web.json_response(data)


@routes.get(r'/contact/{user_id:[\d\w_]+}')
@bot_view_wrapper
async def view(request: web.Request, bot: Wechaty, user_id: str):
    user_id = request.match_info.get('user_id')
    contact: Contact = bot.Contact(user_id)
    await contact.ready()
    return web.json_response(contact.payload.to_dict())


@routes.post(r'/contact/{user_id:[\d\w_]+}/send_message')
@bot_view_wrapper
async def view(request: web.Request, bot: Wechaty, user_id: str):
    contact: Contact = bot.Contact(user_id)
    await contact.ready()
    formdata = await request.post()
    result = await contact.say(formdata.getone('message'))
    return web.json_response(data=dict(msg='Success', data=result.payload.to_dict()))


async def puppetware_start_server(bot, host='0.0.0.0', port=12345):
    context['bot'] = bot

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host, port)
    await site.start()
