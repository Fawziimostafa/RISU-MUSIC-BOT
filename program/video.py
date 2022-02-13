# Copyright (C) 2021 By Risu Music-Project
# Commit Start Date 13/2/2022
# Finished On 13/2/2022


import os
import re
import asyncio
# repository stuff
from config import BOT_USERNAME, IMG_1, IMG_2, IMG_5
from program.utils.inline import stream_markup
from driver.design.thumbnail import thumb
from driver.design.chatname import CHAT_TITLE
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.core import calls, user, bot
from driver.database.dbpunish import is_gbanned_user
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbqueue import add_active_chat, remove_active_chat, music_on
# pyrogram stuff
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message
# py-tgcalls stuff
from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
# youtube-dl stuff
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = data["thumbnails"][0]["url"]
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    user_xd = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if chat_id in await blacklisted_chats():
        await m.reply(
            "ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʙʏ sᴜᴅᴏ ᴜsᴇʀ ᴀɴᴅ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ."
        )
        return await bot.leave_chat(chat_id)
    if await is_gbanned_user(user_id):
        await m.reply_text(f"{user_xd} **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if m.sender_chat:
        return await m.reply_text(
            "ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀɴᴏɴʏᴍᴏᴜs__ ᴜsᴇʀ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ʏᴏᴜʀ ʀᴇᴀʟ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"ᴛᴏ ᴜsᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪssɪᴏɴs**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ messages__\n» ❌ __ɪɴᴠɪᴛᴇ ᴜsᴇʀs__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʏᴘᴇ /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot) 
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **ᴜsᴇʀʙᴏᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀsᴏɴ**: `{e}`"
            )
    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» only 720, 480, 360 allowed\n\n ɴᴏᴡ sᴛʀᴇᴀᴍɪɴɢ ᴠɪᴅᴇᴏ ɪɴ **720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                    duration = convert_seconds(replied.video.duration)
                elif replied.document:
                    songname = replied.document.file_name[:70]
                    duration = convert_seconds(replied.document.duration)
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                await loser.edit("🔄 sᴇᴀʀᴄʜɪɴɢ...")
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"**ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [{songname}]({link}) | `ᴠɪᴅᴇᴏ`\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                )
                os.remove(image)
            else:
                await loser.edit("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid, ctitle)
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await music_on(chat_id)
                await add_active_chat(chat_id)
                await calls.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=image,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🏷 **ɴᴀᴍᴇ:** [{songname}]({link}) | `ᴠɪᴅᴇᴏ`\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                )
                await idle()
                os.remove(image)
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» ʀᴇᴘʟʏ ᴛᴏ ᴀɴ **ᴠɪᴅᴇᴏ ғɪʟᴇ** ᴏʀ **ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍 **sᴇᴀʀᴄʜɪɴɢ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇs ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            await loser.edit("🔄 sᴇᴀʀᴄʜɪɴɢ...")
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f" **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `ᴠɪᴅᴇᴏ`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                            )
                            os.remove(image)
                        else:
                            try:
                                await loser.edit("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
                                await music_on(chat_id)
                                await add_active_chat(chat_id)
                                await calls.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🏷 **ɴᴀᴍᴇ:** [{songname}]({url}) | `ᴠɪᴅᴇᴏ`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🧸 **🎧ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                                )
                                await idle()
                                os.remove(image)
                            except Exception as ep:
                                await loser.delete()
                                await remove_active_chat(chat_id)
                                await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀɴ **ᴠɪᴅᴇᴏ ғɪʟᴇ** ᴏʀ **ɢɪᴠᴇ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ.**"
            )
        else:
            loser = await c.send_message(chat_id, "🔍 **sᴇᴀʀᴄʜɪɴɢ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇs ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        await loser.edit("🔄 sᴇᴀʀᴄʜɪɴɢ...")
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=image,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"**ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `{pos}`\n\n🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `ᴠɪᴅᴇᴏ`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                        )
                        os.remove(image)
                    else:
                        try:
                            await loser.edit("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
                            await music_on(chat_id)
                            await add_active_chat(chat_id)
                            await calls.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🏷️ **ɴᴀᴍᴇ:** [{songname}]({url}) | `ᴠɪᴅᴇᴏ`\n⏱ **ᴅᴜʀᴀᴛɪᴏɴ:** `{duration}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                            )
                            await idle()
                            os.remove(image)
                        except Exception as ep:
                            await loser.delete()
                            await remove_active_chat(chat_id)
                            await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")


@Client.on_message(command(["vstream", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    user_xd = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    if chat_id in await blacklisted_chats():
        await m.reply(
            "ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʙʏ sᴜᴅᴏ ᴜsᴇʀ ᴀɴᴅ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ."
        )
        return await bot.leave_chat(chat_id)
    if await is_gbanned_user(user_id):
        await m.reply_text(f" {user_xd} **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if m.sender_chat:
        return await m.reply_text(
            "ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀɴᴏɴʏᴍᴏᴜs__ ᴜsᴇʀ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ʏᴏᴜʀ ʀᴇᴀʟ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"ᴛᴏ ᴜsᴇ ᴍᴇ, ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ **ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ** ᴡɪᴛʜ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ **ᴘᴇʀᴍɪssɪᴏɴs**:\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n» ❌ __ɪɴᴠɪᴛᴇ ᴜsᴇʀs__\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʏᴘᴇ /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            " ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            " ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "ᴛᴏ ᴜsᴇ ᴍᴇ, ɢɪᴠᴇ ᴍᴇ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴘᴇʀᴍɪssɪᴏɴ ʙᴇʟᴏᴡ:"
            + "\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__\n\nᴏɴᴄᴇ ᴅᴏɴᴇ, ᴛʀʏ ᴀɢᴀɪɴ."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
    except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
            await remove_active_chat(chat_id)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **ᴜsᴇʀʙᴏᴛ ғᴀɪʟᴇᴅ ᴛᴏ ᴊᴏɪɴ**\n\n**ʀᴇᴀsᴏɴ**: `{e}`"
            )

    if len(m.command) < 2:
        await m.reply("» ɢɪᴠᴇ ᴍᴇ ᴀ ʟɪᴠᴇ-ʟɪɴᴋ/ᴍ3ᴜ8 ᴜʀʟ/ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴛᴏ sᴛʀᴇᴀᴍ.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔍 **sᴇᴀʀᴄʜɪɴɢ...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» only 720, 480, 360 ᴀʟʟᴏᴡᴇᴅ\n\n ɴᴏᴡ sᴛʀᴇᴀᴍɪɴɢ ᴠɪᴅᴇᴏ ɪɴ **720p**"
                )
            loser = await c.send_message(chat_id, "🔍 **sᴇᴀʀᴄʜɪɴɢ...**")
        else:
            await m.reply("`/vstream` {link} {720/480/360}")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ ʏᴛ-ᴅʟ ɪssᴜᴇs ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                await loser.edit("🔄 sᴇᴀʀᴄʜɪɴɢ...")
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f" **ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ »** `{pos}`\n\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🧸 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 ᴘʀᴏᴄᴇssɪɴɢ...")
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await calls.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f" **[ᴠɪᴅᴇᴏ ʟɪᴠᴇ]({link}) sᴛʀᴇᴀᴍ sᴛᴀʀᴛᴇᴅ.**\n\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await remove_active_chat(chat_id)
                    await m.reply_text(f"🚫 ᴇʀʀᴏʀ: `{ep}`")
