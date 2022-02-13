from pyrogram.types import Message
from pyrogram import Client, filters

from config import SUDO_USERS, BOT_USERNAME
from driver.core import bot
from driver.filters import command, other_filters
from driver.decorators import sudo_users_only
from driver.database.dblockchat import (
  blacklist_chat,
  blacklisted_chats,
  whitelist_chat,
)


@Client.on_message(command(["block", f"block@{BOT_USERNAME}", "blacklist"]) & ~filters.edited)
@sudo_users_only
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n\n» /block (`ᴄʜᴀᴛ_ɪᴅ`)"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("ᴛʜɪs ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "✅ ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ!"
        )
    await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢs")


@Client.on_message(command(["unblock", f"unblock@{BOT_USERNAME}", "whitelist"]) & ~filters.edited)
@sudo_users_only
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n\n» /unblock (`ᴄʜᴀᴛ_ɪᴅ`)"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("ᴛʜɪs ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "✅ ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ᴡʜɪᴛᴇʟɪsᴛᴇᴅ"
        )
    await message.reply_text(" sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢs")


@Client.on_message(command(["blocklist", f"blocklist@{BOT_USERNAME}", "blacklisted"]) & ~filters.edited)
@sudo_users_only
async def blacklisted_chats_func(_, message: Message):
    text = "📵 » ʙʟᴏᴄᴋᴇᴅ ᴄʜᴀᴛ ʟɪsᴛ:\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await bot.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("❌ ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.")
    else:
        await message.reply_text(text)
