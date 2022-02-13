# credit to TeamYukki for this speedtest module

import os
import wget
import speedtest

from program.utils.formatters import bytes
from driver.filters import command, other_filters
from driver.decorators import sudo_users_only
from config import BOT_USERNAME as bname
from driver.core import bot as app
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(command(["speedtest", f"speedtest@{bname}"]) & ~filters.edited)
@sudo_users_only
async def run_speedtest(_, message: Message):
    m = await message.reply_text("⚡️ ʀᴜɴɴɪɴɢ sᴇʀᴠᴇʀ sᴘᴇᴇᴅᴛᴇsᴛ...")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("⚡️ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴘᴇᴇᴅᴛᴇsᴛ...")
        test.download()
        m = await m.edit("⚡️ ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅᴛᴇsᴛ...")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit(e)
        return
    m = await m.edit("🔄 sʜᴀʀɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ results")
    path = wget.download(result["share"])

    output = f""" **sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪsᴘ:** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ:** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ:**</u>
**ɴᴀᴍᴇ:** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ:** {result['server']['country']}, {result['server']['cc']}
**sᴘᴏɴsᴏʀ:** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ:** {result['server']['latency']}

⚡️ **ᴘɪɴɢ:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
