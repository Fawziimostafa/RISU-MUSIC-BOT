import asyncio

from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.core import user, bot
from driver.filters import command, other_filters
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dbpunish import is_gbanned_user
from driver.database.dbusers import add_served_user
from driver.database.dblockchat import blacklisted_chats
from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, MessageNotModified
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    BOT_NAME = (await c.get_me()).first_name
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ!**")
        return
    await message.reply_text(
        f"""✨ **ᴡᴇʟᴄᴏᴍᴇ {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **ɪs ᴀ ʙᴏᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ɢʀᴏᴜᴘs, ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ!**

**ғɪɴᴅ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ's ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ » 📚 ᴄᴏᴍᴍᴀɴᴅs ʙᴜᴛᴛᴏɴ!**

🔖 **ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ »  ʙᴀsɪᴄ ɢᴜɪᴅᴇ ʙᴜᴛᴛᴏɴ!**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ᴀᴅᴅ 🆁︎ɪsᴜ 🅼︎ᴜsɪᴄ 🅱︎ᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("🔐ʙᴀsɪᴄ ɢᴜɪᴅᴇ", callback_data="user_guide")],
                [
                    InlineKeyboardButton("📚 ᴄᴏᴍᴍᴀɴᴅs", callback_data="command_list"),
                    InlineKeyboardButton("⚕️ᴏᴡɴᴇʀ", url=f"https://t.me/Simple_Mundaa"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 ᴏғғɪᴄɪᴀʟ ɢʀᴏᴜᴘ", url=f"https://t.me/Demon_Support_Group"
                    ),
                    InlineKeyboardButton(
                        "📣 ᴏғғɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/Demon_Creators"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "✳️ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ✳️", url="https://youtube.com/channel/UCtI7hbY-BD7wvuIzoSU0cEw"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    BOT_NAME = (await c.get_me()).first_name
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👥sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/Demon_Support_Group"),
                InlineKeyboardButton(
                    " 📣ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/Demon_Creators"
                ),
            ]
        ]
    )

    alive = f"**ʜᴇʟʟᴏ {message.from_user.mention()}, i'm {BOT_NAME}**\n\ ᴍʏ ᴍᴀsᴛᴇʀ: [{ALIVE_NAME}](https://t.me/{OWNER_USERNAME})\n ʙᴏᴛ ᴠᴇʀsɪᴏɴ: `v{__version__}`\nᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ: `{pyrover}`\n ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ: `{__python_version__}`\n✨ ᴘʏᴛɢᴄᴀʟʟs ᴠᴇʀsɪᴏɴ: `{pytover.__version__}`\n🆙 ᴜᴘᴛɪᴍᴇ sᴛᴀᴛᴜs: `{uptime}`\n\n❤ **ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ʜᴇʀᴇ, ғᴏʀ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ & ᴍᴜsɪᴄ ᴏɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ's ᴠɪᴅᴇᴏ ᴄʜᴀᴛ**"

    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏮 `ᴘᴏɴɢ!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(c: Client, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "⚙️ ʙᴏᴛ sᴛᴀᴛᴜs:\n"
        f"• **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"• **sᴛᴀʀᴛ ᴛɪᴍᴇ:** `{START_TIME_ISO}`"
    )


@Client.on_chat_join_request()
async def approve_join_chat(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    chat_id = m.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if chat_id in await blacklisted_chats():
            await m.reply(
                "ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʙʏ sᴜᴅᴏ ᴜsᴇʀ ᴀɴᴅ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ."
            )
            return await bot.leave_chat(chat_id)
        if member.id == bot_id:
            return await m.reply(
                "🔖 ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ᴛᴏ ᴛʜᴇ **ɢʀᴏᴜᴘ** !\n\n"
                "ᴀᴘᴘᴏɪɴᴛ ᴍᴇ ᴀs ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ɪɴ ᴛʜᴇ **ɢʀᴏᴜᴘ**, ᴏᴛʜᴇʀᴡɪsᴇ ɪ ᴡɪʟʟ ɴᴏᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ, ᴀɴᴅ ᴅᴏɴ'ᴛ ғᴏʀɢᴇᴛ ᴛᴏ ᴛʏᴘᴇ `/userbotjoin` ғᴏʀ ɪɴᴠɪᴛᴇ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ.\n\n"
                "ᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʜᴇɴ ᴛʏᴘᴇ `/reload`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/Demon_Creators"),
                            InlineKeyboardButton("👥sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/Demon_Support_Group")
                        ],
                        [
                            InlineKeyboardButton("🔹✳️ᴀssɪsᴛᴀɴᴛ", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )


chat_watcher_group = 10

@Client.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message: Message):
    if message.from_user:
        user_id = message.from_user.id
        await add_served_user(user_id)
        return
    try:
        userid = message.from_user.id
    except Exception:
        return
    suspect = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"🚦 (> {suspect} <)\n\n**ɢʙᴀɴɴᴇᴅ** ᴜsᴇʀ ᴅᴇᴛᴇᴄᴛᴇᴅ, ᴛʜᴀᴛ ᴜsᴇʀ ʜᴀs ʙᴇᴇɴ ɢʙᴀɴɴᴇᴅ ʙʏ sᴜᴅᴏ ᴜsᴇʀ ᴀɴᴅ ᴡᴀs ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴛʜɪs Chat !\n\n🚫 **ʀᴇᴀsᴏɴ:** ᴘᴏᴛᴇɴᴛɪᴀʟ sᴘᴀᴍᴍᴇʀ ᴀɴᴅ ᴀʙᴜsᴇʀ."
        )
