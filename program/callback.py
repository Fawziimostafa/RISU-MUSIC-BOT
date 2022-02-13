# Copyright (C) 2021 By Risu Music Project

from driver.core import user, bot
from driver.queues import QUEUE
from driver.database.dbpunish import is_gbanned_user
from pyrogram import Client, filters
from program.utils.inline import menu_markup, stream_markup
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_USERNAME,
    UPDATES_CHANNEL,
    SUDO_USERS,
    OWNER_ID,
)


@Client.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    BOT_NAME = (await bot.get_me()).first_name
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ this ʙᴏᴛ", show_alert=True)
        ʀᴇᴛᴜʀɴ
    await query.answer("home start")
    await query.edit_message_text(
        f"""✨ **ᴡᴇʟᴄᴏᴍᴇ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **ɪs ᴀ ʙᴏᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴠɪᴅᴇᴏ ɪɴ ɢʀᴏᴜᴘs, ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ**

**ғɪɴᴅ ᴏᴜᴛ ᴀʟʟ ᴛʜᴇ ʙᴏᴛ's ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ʜᴏᴡ ᴛʜᴇʏ ᴡᴏʀᴋ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ » 📚 ᴄᴏᴍᴍᴀɴᴅs ʙᴜᴛᴛᴏɴ!**

🔖 **ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ »  ʙᴀsɪᴄ ɢᴜɪᴅᴇ ʙᴜᴛᴛᴏɴ!**""",
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


@Client.on_callback_query(filters.regex("quick_use"))
async def quick_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    ass_uname = (await user.get_me()).username
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.answer("quick bot usage")
    await query.edit_message_text(
        f"""ℹ️ ǫᴜɪᴄᴋ ᴜsᴇ ɢᴜɪᴅᴇ ʙᴏᴛ, ᴘʟᴇᴀsᴇ ʀᴇᴀᴅ ғᴜʟʟʏ !

👩🏻‍💼 » /play - ᴛʏᴘᴇ ᴛʜɪs ᴡɪᴛʜ ɢɪᴠᴇ the song ᴛɪᴛʟᴇ ᴏʀ youtube ʟɪɴᴋ ᴏʀ ᴀᴜᴅɪᴏ ғɪʟᴇ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ. (ʀᴇᴍᴇᴍʙᴇʀ ᴛᴏ ᴅᴏɴ'ᴛ ᴘʟᴀʏ ʏᴏᴜᴛᴜʙᴇ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ʙʏ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ, ʙᴇᴄᴀᴜsᴇ ɪᴛ ᴡɪʟʟ ᴄᴀᴜsᴇ ᴜɴғᴏʀᴇsᴇᴇɴ ᴘʀᴏʙʟᴇᴍs.)

👩🏻‍💼 » /vplay - ᴛʏᴘᴇ ᴛʜɪs ᴡɪᴛʜ ɢɪᴠᴇ the song ᴛɪᴛʟᴇ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ. (Remember ᴛᴏ ᴅᴏɴ'ᴛ ᴘʟᴀʏ ʏᴏᴜᴛᴜʙᴇ ʟɪᴠᴇ ᴠɪᴅᴇᴏ ʙʏ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ, ʙᴇᴄᴀᴜsᴇ ɪᴛ ᴡɪʟʟ ᴄᴀᴜsᴇ ᴜɴғᴏʀᴇsᴇᴇɴ ᴘʀᴏʙʟᴇᴍs.)

👩🏻‍💼 » /vstream - ᴛʏᴘᴇ ᴛʜɪs ᴡɪᴛʜ ɢɪᴠᴇ ᴛʜᴇ ʏᴏᴜᴛᴜʙᴇ ʟɪᴠᴇ stream ᴠɪᴅᴇᴏ ʟɪɴᴋ ᴏʀ ᴍ3ᴜ8 ʟɪɴᴋ ᴛᴏ ᴘʟᴀʏ ʟɪᴠᴇ ᴠɪᴅᴇᴏ. (ʀᴇᴍᴇᴍʙᴇʀ ᴛᴏ ᴅᴏɴ'ᴛ ᴘʟᴀʏ ʟᴏᴄᴀʟ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ғɪʟᴇs ᴏʀ ɴᴏɴ-ʟɪᴠᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ʙʏ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ, ʙᴇᴄᴀᴜsᴇ ɪᴛ ᴡɪʟʟ ᴄᴀᴜsᴇ ᴜɴғᴏʀᴇsᴇᴇɴ ᴘʀᴏʙʟᴇᴍs.)

❓ ʜᴀᴠᴇ ǫᴜᴇsᴛɪᴏɴs? ᴄᴏɴᴛᴀᴄᴛ ᴜs ɪɴ [sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ](https://t.me/{GROUP_SUPPORT}).""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("user_guide"))
async def guide_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    ass_uname = (await user.get_me()).username
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.answer("user guide")
    await query.edit_message_text(
        f""" ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ , ʀᴇᴀᴅ ᴛʜᴇ ɢᴜɪᴅᴇ ʙᴇʟᴏᴡ 

1.) ғɪʀsᴛ, ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
2.) ᴛʜᴇɴ, ᴘʀᴏᴍᴏᴛᴇ ᴛʜɪs ʙᴏᴛ ᴀs ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ᴏɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴀʟsᴏ give all permissions except Anonymous admin.
3.) ᴀғᴛᴇʀ ᴘʀᴏᴍᴏᴛɪɴɢ this ʙᴏᴛ, ᴛʏᴘᴇ /reload ɪɴ ɢʀᴏᴜᴘ ᴛᴏ ᴜᴘᴅᴀᴛᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴅᴀᴛᴀ.
3.) ɪɴᴠɪᴛᴇ @{ass_uname} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴛʏᴘᴇ /userbotjoin ᴛᴏ ɪɴᴠɪᴛᴇ ʜᴇʀ, ᴜɴғᴏʀᴛᴜɴᴀᴛᴇʟʏ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴡɪʟʟ ᴊᴏɪɴᴇᴅ ʙʏ ɪᴛsᴇʟғ ᴡʜᴇɴ ʏᴏᴜ ᴛʏᴘᴇ `/play (sᴏɴɢ ɴᴀᴍᴇ)` ᴏʀ `/vplay (sᴏɴɢ ɴᴀᴍᴇ)`.
4.) ᴛᴜʀɴ ᴏɴ/Start ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ғɪʀsᴛ ʙᴇғᴏʀᴇ sᴛᴀʀᴛ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ/ᴍᴜsɪᴄ.

`- END, EVERYTHING HAS BEEN SETUP -`

📌 ɪғ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ, ᴍᴀᴋᴇ sᴜʀᴇ ɪғ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴛᴜʀɴᴇᴅ ᴏɴ ᴀɴᴅ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.

 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀ ғᴏʟʟᴏᴡ-ᴜᴘ ǫᴜᴇsᴛɪᴏɴs ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ ᴛᴇʟʟ ɪᴛ ᴏɴ ᴍʏ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ ʜᴇʀᴇ: @{GROUP_SUPPORT}.""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="home_start")]]
        ),
    )


@Client.on_callback_query(filters.regex("command_list"))
async def commands_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **ʜᴇʟʟᴏ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) **

» ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇᴀᴅ ᴛʜᴇ ᴍᴏᴅᴜʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ & sᴇᴇ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs 

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ (`! / .`) ʜᴀɴᴅʟᴇʀ""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("» ǫᴜɪᴄᴋ ᴜsᴇ ɢᴜɪᴅᴇ «", callback_data="quick_use"),
                ],[
                    InlineKeyboardButton("👮🏻‍♀️ ᴀᴅᴍɪɴs ᴄᴏᴍᴍᴀɴᴅs", callback_data="admin_command"),
                ],[
                    InlineKeyboardButton("👩🏻‍💼 ᴜsᴇʀs ᴄᴏᴍᴍᴀɴᴅs", callback_data="user_command"),
                ],[
                    InlineKeyboardButton("☣️sᴜᴅᴏ ᴄᴏᴍᴍᴀɴᴅs", callback_data="sudo_command"),
                    InlineKeyboardButton("🔐ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅs", callback_data="owner_command"),
                ],[
                    InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="home_start")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("user_command"))
async def user_set(_, query: CallbackQuery):
    BOT_NAME = (await bot.get_me()).first_name
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.answer("basic commands")
    await query.edit_message_text(
        f"""✏️ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ ғᴏʀ ᴀʟʟ ᴜsᴇʀ.

» /play (song name/link) - ᴘʟᴀʏ ᴍᴜsɪᴄ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ
» /vplay (video name/link) - ᴘʟᴀʏ ᴠɪᴅᴇᴏ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ
» /vstream (m3u8/yt live link) - ᴘʟᴀʏ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ
» /playlist - sᴇᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ sᴏɴɢ
» /lyric (query) - sᴄʀᴀᴘ ᴛʜᴇ sᴏɴɢ ʟʏʀɪᴄ
» /video (query) - ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
» /song (query) - ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
» /search (query) - sᴇᴀʀᴄʜ ᴀ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ʟɪɴᴋ
» /ping - sʜᴏᴡ ᴛʜᴇ ʙᴏᴛ ᴘɪɴɢ sᴛᴀᴛᴜs
» /uptime - sʜᴏᴡ ᴛʜᴇ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ sᴛᴀᴛᴜs
» /alive - sʜᴏᴡ ᴛʜᴇ ʙᴏᴛ ᴀʟɪᴠᴇ ɪɴғᴏ (ɪɴ ɢʀᴏᴜᴘ ᴏɴʟʏ)

⚡️ __ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} ᴀɪ__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("admin_command"))
async def admin_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    BOT_NAME = (await bot.get_me()).first_name
    if await is_gbanned_user(user_id):
        await query.answer("ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.answer("admin commands")
    await query.edit_message_text(
        f"""✏️ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ ғᴏʀ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ.

» /pause - ᴘᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ ʙᴇɪɴɢ ᴘʟᴀʏᴇᴅ
» /resume - ᴘʟᴀʏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜsʟʏ ᴘᴀᴜsᴇᴅ ᴛʀᴀᴄᴋ
» /skip - ɢᴏᴇs ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ 
» /stop - sᴛᴏᴘ ᴘʟᴀʏʙᴀᴄᴋ ᴏғ ᴛʜᴇ ᴛʀᴀᴄᴋ ᴀɴᴅ ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ
» /vmute - ᴍᴜᴛᴇ ᴛʜᴇ sᴛʀᴇᴀᴍᴇʀ ᴜsᴇʀʙᴏᴛ ᴏɴ ɢʀᴏᴜᴘ ᴄᴀʟʟ
» /vunmute - ᴜɴᴍᴜᴛᴇ ᴛʜᴇ sᴛʀᴇᴀᴍᴇʀ ᴜsᴇʀʙᴏᴛ ᴏɴ ɢʀᴏᴜᴘ ᴄᴀʟʟ
» /volume `1-200` - ᴀᴅᴊᴜsᴛ ᴛʜᴇ ᴠᴏʟᴜᴍᴇ ᴏғ ᴍᴜsɪᴄ (ᴜsᴇʀʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴀᴅᴍɪɴ)
» /reload - ʀᴇʟᴏᴀᴅ ʙᴏᴛ ᴀɴᴅ ʀᴇғʀᴇsʜ ᴛʜᴇ ᴀᴅᴍɪɴ ᴅᴀᴛᴀ
» /userbotjoin - ɪɴᴠɪᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴛᴏ ᴊᴏɪɴ ɢʀᴏᴜᴘ
» /userbotleave - ᴏʀᴅᴇʀ ᴜsᴇʀʙᴏᴛ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ɢʀᴏᴜᴘ

⚡️ __ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("sudo_command"))
async def sudo_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    BOT_NAME = (await bot.get_me()).first_name
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    if user_id not in SUDO_USERS:
        await query.answer("⚠️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴄʟɪᴄᴋ ᴛʜɪs ʙᴜᴛᴛᴏɴ\n\n» ᴛʜɪs ʙᴜᴛᴛᴏɴ ɪs ʀᴇsᴇʀᴠᴇᴅ ғᴏʀ sᴜᴅᴏ ᴍᴇᴍʙᴇʀs ᴏғ ᴛʜɪs ʙᴏᴛ.", show_alert=True)
        Return
    await query.answer("sudo commands")
    await query.edit_message_text(
        f"""✏️ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ ғᴏʀ sᴜᴅᴏ ᴜsᴇʀ.

» /stats - ɢᴇᴛ ᴛʜᴇ ʙᴏᴛ ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛɪsᴛɪᴄ
» /calls - sʜᴏᴡ ʏᴏᴜ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀʟʟ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ
» /block (`ᴄʜᴀᴛ_ɪᴅ`) - ᴜsᴇ ᴛʜɪs ᴛᴏ ʙʟᴀᴄᴋʟɪsᴛ ᴀɴʏ ɢʀᴏᴜᴘ ғʀᴏᴍ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ
» /unblock (`ᴄʜᴀᴛ_ɪᴅ`) - ᴜsᴇ ᴛʜɪs ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ᴀɴʏ ɢʀᴏᴜᴘ ғʀᴏᴍ ᴜsɪɴɢ ʏᴏᴜʀ ʙᴏᴛ
» /blocklist - sʜᴏᴡ ʏᴏᴜ ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀʟʟ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ
» /speedtest - ʀᴜɴ ᴛʜᴇ ʙᴏᴛ sᴇʀᴠᴇʀ sᴘᴇᴇᴅᴛᴇsᴛ
» /sysinfo - sʜᴏᴡ ᴛʜᴇ sʏsᴛᴇᴍ ɪɴғᴏʀᴍᴀᴛɪᴏɴ
» /eval - ᴇxᴇᴄᴜᴛᴇ ᴀɴʏ ᴄᴏᴅᴇ (`ᴅᴇᴠᴇʟᴏᴘᴇʀ sᴛᴜғғ`)
» /sh - ʀᴜɴ ᴀɴʏ ᴄᴏᴍᴍᴀɴᴅ (`ᴅᴇᴠᴇʟᴏᴘᴇʀ sᴛᴜғғ`)

⚡ __ᴘᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} ᴀɪ__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("owner_command"))
async def owner_set(_, query: CallbackQuery):
    user_id = query.from_user.id
    BOT_NAME = (await bot.get_me()).first_name
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    if user_id not in OWNER_ID:
        await query.answer("⚠️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴄʟɪᴄᴋ ᴛʜɪs ʙᴜᴛᴛᴏɴ\n\n» ᴛʜɪs ʙᴜᴛᴛᴏɴ ɪs ʀᴇsᴇʀᴠᴇᴅ ғᴏʀ ᴏᴡɴᴇʀ ᴏғ ᴛʜɪs ʙᴏᴛ.", show_alert=True)
        return
    await query.answer("owner commands")
    await query.edit_message_text(
        f"""✏️ ᴄᴏᴍᴍᴀɴᴅ ʟɪsᴛ ғᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ.

» /gban (`ᴜsᴇʀɴᴀᴍᴇ` ᴏʀ `ᴜsᴇʀ_ɪᴅ`) - ғᴏʀ ɢʟᴏʙᴀʟ ʙᴀɴɴᴇᴅ ᴘᴇᴏᴘʟᴇ, ᴄᴀɴ be ᴜsᴇᴅ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ
» /ungban (`ᴜsᴇʀɴᴀᴍᴇ` ᴏʀ `ᴜsᴇʀ_ɪᴅ`) - ғᴏʀ ᴜɴ-ɢʟᴏʙᴀʟ ʙᴀɴɴᴇᴅ ᴘᴇᴏᴘʟᴇ, ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ
» /update - ᴜᴘᴅᴀᴛᴇ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏ ʟᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ
» /restart - ʀᴇsᴛᴀʀᴛ ʏᴏᴜʀ ʙᴏᴛ ᴅɪʀᴇᴄᴛʟʏ
» /leaveall - ᴏʀᴅᴇʀ ᴜsᴇʀʙᴏᴛ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ᴀʟʟ ɢʀᴏᴜᴘ
» /leavebot (`ᴄʜᴀᴛ ɪᴅ`) - ᴏʀᴅᴇʀ ʙᴏᴛ ᴛᴏ ʟᴇᴀᴠᴇ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ ʏᴏᴜ sᴘᴇᴄɪғʏ
» /broadcast (`ᴍᴇssᴀɢᴇ`) - sᴇɴᴅ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘs ɪɴ ʙᴏᴛ ᴅᴀᴛᴀʙᴀsᴇ
» /broadcast_pin (`ᴍᴇssᴀɢᴇ`) - sᴇɴᴅ ᴀ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ɢʀᴏᴜᴘs ɪɴ ʙᴏᴛ ᴅᴀᴛᴀʙᴀsᴇ ᴡɪᴛʜ ᴛʜᴇ ᴄʜᴀᴛ ᴘɪɴ

⚡ __Powered by {BOT_NAME} AI__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="command_list")]]
        ),
    )


@Client.on_callback_query(filters.regex("stream_menu_panel"))
async def at_set_markup_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.message.from_user.id
    buttons = menu_markup(user_id)
    if chat_id in QUEUE:
        await query.answer("control panel opened")
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_callback_query(filters.regex("stream_home_panel"))
async def is_set_home_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    await query.answer("control panel closed")
    user_id = query.message.from_user.id
    buttons = stream_markup(user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("set_close"))
async def on_close_menu(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    await query.message.delete()


@Client.on_callback_query(filters.regex("close_panel"))
async def in_close_panel(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer("ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    await query.message.delete()
