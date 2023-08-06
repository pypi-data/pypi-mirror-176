"""
import logging
from datetime import datetime
from traceback import format_exc
import pytz
from pyrogram import ContinuePropagation, StopPropagation, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from pyrogram.handlers import MessageHandler

from config import Var
from AyiinXd import *
from AyiinXd.ayiin import eor


async def is_admin_or_owner(message, user_id) -> bool:
    '''Check If A User Is Creator Or Admin Of The Current Group'''
    if message.chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR):
        return True
    return False


def Ayiin(
    cmd: list,
    group: int = 0,
    devs: bool = False,
    pm_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    admin_only: bool = False,
    pass_error: bool = False,
    propagate_to_next_handler: bool = True,
):
    '''- Main Decorator To Register Commands. -'''
    if not devs:
        filterm = (
            filters.me
            & filters.command(cmd, Var.HNDLR)
            & ~filters.via_bot
            & ~filters.forwarded
        )
    else:
        filterm = (
            filters.user(DEVS)
            & filters.command(cmd, "")
        )

    def decorator(func):
        async def wrapper(client, message):
            message.client = client
            chat_type = message.chat.type
            if admin_only and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await eor(
                    message, "<code>This Command Only Works, If You Are Admin Of The Chat!</code>"
                )
                return
            if group_only and chat_type != (
                    ChatType.GROUP or ChatType.SUPERGROUP):
                await eor(message, "<code>Are you sure this is a group?</code>")
                return
            if channel_only and chat_type != ChatType.CHANNEL:
                await eor(message, "This Command Only Works In Channel!")
                return
            if pm_only and chat_type != ChatType.PRIVATE:
                await eor(message, "<code>This Cmd Only Works On PM!</code>")
                return
            if pass_error:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "Please Don't Delete Commands While it's Processing..."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException:
                    logging.error(
                        f"Exception - {func.__module__} - {func.__name__}"
                    )
                    TZZ = pytz.timezone(Var.TZ)
                    datetime_tz = datetime.now(TZZ)
                    text = "<b>!ERROR - REPORT!</b>\n\n"
                    text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                    text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                    text += f"\n<b>Plugin-Name :</b> <code>{func.__module__}</code>"
                    text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                    text += datetime_tz.strftime(
                        "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                    )
                    try:
                        xx = await tgbot.send_message(Var.LOG_CHAT, text)
                        await xx.pin(disable_notification=False)
                    except BaseException:
                        logging.error(text)
        add_handler(filterm, wrapper, cmd)
        return wrapper

    return decorator


def listen(filter_s):
    '''Simple Decorator To Handel Custom Filters'''
    def decorator(func):
        async def wrapper(client, message):
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}")
                TZZ = pytz.timezone(Var.TZ)
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR WHILE HANDLING UPDATES!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await tgbot.send_message(Var.LOG_CHAT, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        if AYIIN1:
            AYIIN1.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN2:
            AYIIN2.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN3:
            AYIIN3.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN4:
            AYIIN4.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN5:
            AYIIN5.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN6:
            AYIIN6.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN7:
            AYIIN7.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN8:
            AYIIN8.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN9:
            AYIIN9.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN10:
            AYIIN10.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN11:
            AYIIN11.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN12:
            AYIIN12.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN13:
            AYIIN13.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN14:
            AYIIN14.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN15:
            AYIIN15.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN16:
            AYIIN16.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN17:
            AYIIN17.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN18:
            AYIIN18.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN19:
            AYIIN19.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN20:
            AYIIN20.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN21:
            AYIIN21.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN22:
            AYIIN22.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN23:
            AYIIN23.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN24:
            AYIIN24.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN25:
            AYIIN25.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN26:
            AYIIN26.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN27:
            AYIIN27.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN28:
            AYIIN28.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN29:
            AYIIN29.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN30:
            AYIIN30.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN31:
            AYIIN31.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN32:
            AYIIN32.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN33:
            AYIIN33.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN34:
            AYIIN34.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN35:
            AYIIN35.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN36:
            AYIIN36.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN37:
            AYIIN37.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN38:
            AYIIN38.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN39:
            AYIIN39.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN40:
            AYIIN40.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN41:
            AYIIN41.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN42:
            AYIIN42.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN43:
            AYIIN43.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN44:
            AYIIN44.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN45:
            AYIIN45.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN46:
            AYIIN46.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN47:
            AYIIN47.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN48:
            AYIIN48.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN49:
            AYIIN49.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN50:
            AYIIN50.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        return wrapper

    return decorator


def add_handler(filter_s, func_, cmd):
    if AYIIN1:
        AYIIN1.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN2:
        AYIIN2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN3:
        AYIIN3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN4:
        AYIIN4.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN5:
        AYIIN5.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN6:
        AYIIN6.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN7:
        AYIIN7.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN8:
        AYIIN8.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN9:
        AYIIN9.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN10:
        AYIIN10.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN11:
        AYIIN11.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN12:
        AYIIN12.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN13:
        AYIIN13.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN14:
        AYIIN14.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN15:
        AYIIN15.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN16:
        AYIIN16.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN17:
        AYIIN17.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN18:
        AYIIN18.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN19:
        AYIIN19.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN20:
        AYIIN20.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN21:
        AYIIN21.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN22:
        AYIIN22.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN23:
        AYIIN23.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN24:
        AYIIN24.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN25:
        AYIIN25.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN26:
        AYIIN26.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN27:
        AYIIN27.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN28:
        AYIIN28.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN29:
        AYIIN29.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN30:
        AYIIN30.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN31:
        AYIIN31.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN32:
        AYIIN32.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN33:
        AYIIN33.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN34:
        AYIIN34.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN35:
        AYIIN35.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN36:
        AYIIN36.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN37:
        AYIIN37.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN38:
        AYIIN38.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN39:
        AYIIN39.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN40:
        AYIIN40.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN41:
        AYIIN41.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN42:
        AYIIN42.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN43:
        AYIIN43.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN44:
        AYIIN44.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN45:
        AYIIN45.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN46:
        AYIIN46.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN47:
        AYIIN47.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN48:
        AYIIN48.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN49:
        AYIIN49.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN50:
        AYIIN50.add_handler(MessageHandler(func_, filters=filter_s), group=0)
"""
