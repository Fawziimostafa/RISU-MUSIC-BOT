""" broadcast & statistic collector """


import asyncio

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover

from pytgcalls import (__version__ as pytgver)
from program import __version__ as ver
from program.start import __python_version__ as pyver

from driver.filters import command
from driver.decorators import bot_creator, sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count
from driver.database.dbqueue import get_active_chats

from config import BOT_USERNAME as uname


@Client.on_message(command(["broadcast", f"broadcast@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_nopin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ ɪɴ {sent} ɢʀᴏᴜᴘ.")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ**:\n\n/ʙʀᴏᴀᴅᴄᴀsᴛ (`ᴍᴇssᴀɢᴇ`) or (`ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ ɪɴ {sent} ɢʀᴏᴜᴘ.")


@Client.on_message(command(["broadcast_pin", f"broadcast_pin@{uname}"]) & ~filters.edited)
@bot_creator
async def broadcast_message_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ ɪɴ {sent} ɢʀᴏᴜᴘ.\n📌 sᴇɴᴛ ᴡɪᴛʜ {pin} ᴄʜᴀᴛ ᴘɪɴs."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**ᴜsᴀɢᴇ**:\n\n/ʙʀᴏᴀᴅᴄᴀsᴛ_ᴘɪɴ (`ᴍᴇssᴀɢᴇ`) ᴏʀ (`ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"✅ ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ ɪɴ {sent} ɢʀᴏᴜᴘ.\n📌 sᴇɴᴛ ᴡɪᴛʜ {pin} ᴄʜᴀᴛ ᴘɪɴs."
    )


@Client.on_message(command(["stats", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def bot_statistic(c: Client, message: Message):
    name = (await c.get_me()).first_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await c.send_message(
        chat_id, "❖ ᴄᴏʟʟᴇᴄᴛɪɴɢ sᴛᴀᴛs..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛɪsᴛɪᴄ ᴏғ [{name}](https://t.me/{uname})`:`

✪ **ɢʀᴏᴜᴘs ᴄʜᴀᴛ** : `{served_chats}`
✪ **ᴜsᴇʀs ᴅɪᴀʟᴏɢ** : `{served_users}`
✪ **ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs** : `{gbans_usertl}`

✪ **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ** : `{pyver}`
✪ **ᴘʏᴛɢᴄᴀʟʟs ᴠᴇʀsɪᴏɴ** : `{pytgver.__version__}`
✪ **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ** : `{pyrover}`

✪ ʙᴏᴛ ᴠᴇʀsɪᴏɴ: `{ver}`"""
    
    await msg.edit(tgm, disable_web_page_preview=True)


@Client.on_message(command(["calls", f"calls@{uname}"]) & ~filters.edited)
@sudo_users_only
async def active_calls(c: Client, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"🚫 ᴇʀʀᴏʀ: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await c.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await c.get_chat(x)).username:
            user = (await c.get_chat(x)).username
            text += (
                f"**{j + 1}.** [{title}](https://t.me/{user}) [`{x}`]\n"
            )
        else:
            text += f"**{j + 1}.** {title} [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟs")
    else:
        await message.reply_text(
            f"✏️ **ʀᴜɴɴɪɴɢ ɢʀᴏᴜᴘ ᴄᴀʟʟ ʟɪsᴛ:**\n\n{text}\n\n❖ ᴛʜɪs ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀʟʟ ᴄᴜʀʀᴇɴᴛ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ.",
            disable_web_page_preview=True,
        )
