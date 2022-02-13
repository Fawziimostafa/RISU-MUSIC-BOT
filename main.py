import asyncio
from pytgcalls import idle
from driver.core import calls, bot, user


async def start_bot():
    await bot.start()
    print("[INFO]: ʙᴏᴛ & ᴜʙᴏᴛ ᴄʟɪᴇɴʏ sᴛᴀʀᴛᴇᴅ")
    await calls.start()
    print("[INFO]: ᴘʏ-ᴛɢᴄᴀʟʟs ᴄʟɪᴇɴᴛ sᴛᴀʀᴛ")
    await user.join_chat("Demon_Support_Group")
    await user.join_chat("Demon_Creators")
    await idle()
    print("[INFO]: sᴛᴏᴘɪɴɢ ʙᴏᴛ & ᴜsᴇʀʙᴏᴛ")
    await bot.stop()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
