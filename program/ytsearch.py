from config import BOT_USERNAME
from driver.filters import command
from driver.database.dbpunish import is_gbanned_user
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch


@Client.on_message(command(["search", f"search@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if len(message.command) < 2:
        return await message.reply_text("/search **ɴᴇᴇᴅs ᴀɴ ᴀʀɢᴜᴍᴇɴᴛ**")
    query = message.text.split(None, 1)[1]
    m = await message.reply_text("🔎 **sᴇᴀʀᴄʜɪɴɢ...**")
    results = YoutubeSearch(query, max_results=5).to_dict()
    text = ""
    for i in range(5):
        try:
            text += f"🏷 **ɴᴀᴍᴇ:** __{results[i]['title']}__\n"
            text += f"⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{results[i]['duration']}`\n"
            text += f"👀 **ᴠɪᴇᴡs:** `{results[i]['views']}`\n"
            text += f"📣 **ᴄʜᴀɴɴᴇʟ:** {results[i]['channel']}\n"
            text += f"🔗: https://www.youtube.com{results[i]['url_suffix']}\n\n"
        except IndexError:
            break
    await m.edit_text(
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_panel")]]
        ),
    )
