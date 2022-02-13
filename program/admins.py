import os
from cache.admins import admins
from driver.core import calls, bot
from pyrogram import Client, filters
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.queues import QUEUE, clear_queue
from driver.filters import command, other_filters
from driver.decorators import authorized_users_only
from driver.utils import skip_current_song, skip_item
from driver.database.dbpunish import is_gbanned_user

from driver.database.dbqueue import (
    is_music_playing,
    remove_active_chat,
    music_off,
    music_on,
)
from program.utils.inline import (
    stream_markup,
    close_mark,
    back_mark,
)
from config import (
    BOT_USERNAME,
    GROUP_SUPPORT,
    IMG_5,
    UPDATES_CHANNEL,
)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message: Message):
    global admins
    new_admins = []
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ ʙᴏᴛ **ʀᴇʟᴏᴀᴅᴇᴅ ᴄᴏʀʀᴇᴄᴛʟʏ **\n✅ **ᴀᴅᴍɪɴ ʟɪsᴛ** ʜᴀs **ᴜᴘᴅᴀᴛᴇᴅ **"
    )


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ʜᴀs ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ.")
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await m.reply(" ᴛʜᴇ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ.")
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await m.reply(
                "⏸ **ᴛʀᴀᴄᴋ ᴘᴀᴜsᴇᴅ.**\n\n• **ᴛᴏ ʀᴇsᴜᴍᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ, ᴜsᴇ ᴛʜᴇ**\n» /resume ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await m.reply(" ᴛʜᴇ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ.")
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await m.reply(
                "▶️ **ᴛʀᴀᴄᴋ ʀᴇsᴜᴍᴇᴅ.**\n\n• **ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ sᴛʀᴇᴀᴍ, ᴜsᴇ ᴛʜᴇ**\n» /pause ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(c: Client, m: Message):
    await m.delete()
    user_id = m.from_user.id
    chat_id = m.chat.id
    user_xd = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if await is_gbanned_user(user_id):
        await m.reply_text(f" {user_xd} **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await c.send_message(chat_id, "❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ")
        elif op == 1:
            await c.send_message(chat_id, "» ᴛʜᴇʀᴇ's ɴᴏ ᴍᴏʀᴇ ᴍᴜsɪᴄ ɪɴ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ, ᴜsᴇʀʙᴏᴛ ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ.")
        elif op == 2:
            await c.send_message(chat_id, "🗑️ ᴄʟᴇᴀʀɪɴɢ ᴛʜᴇ **ǫᴜᴇᴜᴇs**\n\n**• ᴜsᴇʀʙᴏᴛ** ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ.")
        else:
            buttons = stream_markup(user_id)
            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
            thumbnail = f"{IMG_5}"
            title = f"{op[0]}"
            userid = m.from_user.id
            gcname = m.chat.title
            ctitle = await CHAT_TITLE(gcname)
            image = await thumb(thumbnail, title, userid, ctitle)
            await c.send_photo(
                chat_id,
                photo=image,
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"⏭ **sᴋɪᴘᴘᴇᴅ** ᴛᴏ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ.\n\n🏷️ **ɴᴀᴍᴇ:** [{op[0]}]({op[1]})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
            )
            os.remove(image)
    else:
        skip = m.text.split(None, 1)[1]
        track = "🗑 ʀᴇᴍᴏᴠᴇᴅ sᴏɴɢ ғʀᴏᴍ ǫᴜᴇᴜᴇ:"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    data = await skip_item(chat_id, x)
                    if data == 0:
                        pass
                    else:
                        track = track + "\n" + f"**#{x}** - {hm}"
            await m.reply(track)


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await m.reply(" ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ.")
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await m.reply(
                "🔇 **ᴜsᴇʀʙᴏᴛ ᴍᴜᴛᴇᴅ.**\n\n• **ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ, ᴜsᴇ ᴛʜᴇ**\n» /unmute ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await m.reply(" ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴜɴᴍᴜᴛᴇᴅ.")
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await m.reply(
                "🔊 **ᴜsᴇʀʙᴏᴛ ᴜɴᴍᴜᴛᴇᴅ.**\n\n• **ᴛᴏ ᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ, ᴜsᴇ ᴛʜᴇ**\n» /mute ᴄᴏᴍᴍᴀɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ...**")


@Client.on_callback_query(filters.regex("set_pause"))
async def cbpause(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer(" ᴛʜᴇ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ.", show_alert=True)
                return
            await calls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer("⏸ ᴛʜᴇ ᴍᴜsɪᴄ ʜᴀs ᴘᴀᴜsᴇᴅ !\n\n» ᴛᴏ ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴍᴜsɪᴄ ᴄʟɪᴄᴋ ᴏɴ ʀᴇsᴜᴍᴇ ʙᴜᴛᴛᴏɴ ", show_alert=True)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_callback_query(filters.regex("set_resume"))
async def cbresume(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer(" ᴛʜᴇ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ.", show_alert=True)
                return
            await calls.resume_stream(chat_id)
            await music_on(chat_id)
            await query.answer("▶️ ᴛʜᴇ ᴍᴜsɪᴄ ʜᴀs ʀᴇsᴜᴍᴇᴅ !\n\n» ᴛᴏ ᴘᴀᴜsᴇ ᴛʜᴇ ᴍᴜsɪᴄ ᴄʟɪᴄᴋ ᴏɴ ᴘᴀᴜsᴇ ʙᴜᴛᴛᴏɴ ", show_alert=True)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_callback_query(filters.regex("set_stop"))
async def cbstop(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await calls.leave_group_call(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **ᴛʜɪs sᴛʀᴇᴀᴍɪɴɢ ʜᴀs ᴇɴᴅᴇᴅ**", reply_markup=close_mark)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_callback_query(filters.regex("set_mute"))
async def cbmute(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if not await is_music_playing(chat_id):
                await query.answer(" ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ.", show_alert=True)
                return
            await calls.mute_stream(chat_id)
            await music_off(chat_id)
            await query.answer("🔇 ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ʜᴀs ᴍᴜᴛᴇᴅ !\n\n» ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴄʟɪᴄᴋ ᴏɴ ᴜɴᴍᴜᴛᴇ ʙᴜᴛᴛᴏɴ ", show_alert=True)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_callback_query(filters.regex("set_unmute"))
async def cbunmute(_, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_gbanned_user(user_id):
        await query.answer(" ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ", show_alert=True)
        return
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(" ᴏɴʟʏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴘᴇʀᴍɪssɪᴏɴ ᴛʜᴀᴛ ᴄᴀɴ ᴛᴀᴘ ᴛʜɪs ʙᴜᴛᴛᴏɴ ", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            if await is_music_playing(chat_id):
                await query.answer("ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴜɴᴍᴜᴛᴇᴅ.", show_alert=True)
                return
            await calls.unmute_stream(chat_id)
            await music_on(chat_id)
            await query.answer("🔊 ᴛʜᴇ sᴛʀᴇᴀᴍ ᴜsᴇʀʙᴏᴛ ʜᴀs ᴜɴᴍᴜᴛᴇᴅ !\n\n» ᴛᴏ ᴍᴜᴛᴇ ᴛʜᴇ ᴜsᴇʀʙᴏᴛ ᴄʟɪᴄᴋ ᴏɴ ᴍᴜᴛᴇ ʙᴜᴛᴛᴏɴ ", show_alert=True)
        except Exception as e:
            await query.edit_message_text(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`", reply_markup=close_mark)
    else:
        await query.answer("❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ...", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    user_id = m.from_user.id
    if await is_gbanned_user(user_id):
        await m.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if len(m.command) < 2:
        await m.reply_text("ᴜsᴀɢᴇ: `/volume` (`0-200`)")
        return
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **ᴠᴏʟᴜᴍᴇ sᴇᴛ ᴛᴏ** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **ᴇʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **ɴᴏᴛʜɪɴɢ ɪɴ ᴘʟᴀʏɪɴɢ...**")
