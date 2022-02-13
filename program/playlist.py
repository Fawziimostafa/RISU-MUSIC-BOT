# Copyright (C) 2021 By Risu Music-Project
# Commit Start Date 13/2/2022
# Finished On 13/2/2022

from config import BOT_USERNAME
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from pyrogram import Client, filters
from driver.queues import QUEUE, get_queue
from driver.filters import command, other_filters
from driver.database.dbpunish import is_gbanned_user


keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="set_close")]]
)


@Client.on_message(command(["playlist", f"playlist@{BOT_USERNAME}", "queue", f"queue@{BOT_USERNAME}"]) & other_filters)
async def playlist(client, m: Message):
    chat_id = m.chat.id
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue)==1:
            await m.reply(f" **ᴄᴜʀʀᴇɴᴛʟʏ sᴛʀᴇᴀᴍɪɴɢ**`:`\n\n*️⃣ [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`", reply_markup=keyboard, disable_web_page_preview=True)
        else:
            QUE = f" **ᴄᴜʀʀᴇɴᴛʟʏ sᴛʀᴇᴀᴍɪɴɢ**`:`\n\n*️⃣ [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**📖 ǫᴜᴇᴜᴇ sᴏɴɢ ʟɪsᴛ**`:`\n"
            l = len(chat_queue)
            for x in range (1, l):
                han = chat_queue[x][0]
                hok = chat_queue[x][2]
                hap = chat_queue[x][3]
                QUE = QUE + "\n" + f"`#{x}` - [{han}]({hok}) | `{hap}`"
            await m.reply(QUE, reply_markup=keyboard, disable_web_page_preview=True)
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ sᴛʀᴇᴀᴍɪɴɢ.**")
