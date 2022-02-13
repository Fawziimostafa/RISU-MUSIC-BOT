# Copyright (C) 2021 By Risu Music-Project

import os
import re
import time
import asyncio
import lyricsgenius

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from config import BOT_USERNAME as bn
from driver.filters import command, other_filters
from driver.database.dbpunish import is_gbanned_user


@Client.on_message(command(["song", f"song@{bn}"]) & ~filters.edited)
async def song_downloader(_, message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    await message.delete()
    query = " ".join(message.command[1:])
    m = await message.reply("🔎 ғɪɴᴅɪɴɢ sᴏɴɢ...")
    ydl_ops = {
        'format': 'bestaudio[ext=m4a]',
        'keepvideo': True,
        'prefer_ffmpeg': False,
        'geo_bypass': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("❌ sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ.\n\n» ɢɪᴠᴇ ᴍᴇ ᴀ ᴠᴀʟɪᴅ sᴏɴɢ ɴᴀᴍᴇ ")
        print(str(e))
        return
    await m.edit("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ sᴏɴɢ...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"• uploader @{bn}"
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ sᴏɴɢ...")
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=host,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        await m.delete()

    except Exception as e:
        await m.edit("❌ ᴇʀʀᴏʀ, ᴡᴀɪᴛ ғᴏʀ ʙᴏᴛ ᴏᴡɴᴇʀ ᴛᴏ ғɪx")
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(
    command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
async def video_downloader(_, message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    await message.delete()
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 ᴇʀʀᴏʀ: `{e}`")
    preview = wget.download(thumbnail)
    await msg.edit("📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


@Client.on_message(command(["lyric", f"lyric@{bn}", "lyrics"]))
async def get_lyric_genius(_, message: Message):
    user_id = message.from_user.id
    if await is_gbanned_user(user_id):
        await message.reply_text(" **ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ**")
        return
    if len(message.command) < 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n\n/ʟʏʀɪᴄs (sᴏɴɢ ɴᴀᴍᴇ)")
    m = await message.reply_text("🔍 sᴇᴀʀᴄʜɪɴɢ ʟʏʀɪᴄs...")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("❌ `404` ʟʏʀɪᴄs ɴᴏᴛ ғᴏᴜɴᴅ")
    xxx = f"""
**sᴏɴɢ ɴᴀᴍᴇ:** __{query}__
**ᴀʀᴛɪsᴛ ɴᴀᴍᴇ:** {S.artist}
**__ʟʏʀɪᴄs:__**
{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`attached lyrics text`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)
