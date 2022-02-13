""" global banned and un-global banned module """


import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from driver.filters import command, other_filters
from driver.decorators import bot_creator
from driver.database.dbchat import get_served_chats
from driver.database.dbpunish import add_gban_user, is_gbanned_user, remove_gban_user

from config import SUDO_USERS, BOT_USERNAME as bn


@Client.on_message(command(["gban", f"gban@{bn}"]) & other_filters)
@bot_creator
async def global_banned(c: Client, message: Message):
    BOT_NAME = (await c.get_me()).first_name
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**ᴜsᴀɢᴇ:**\n\n/gban [username | user_id]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await c.get_users(user)
        from_user = message.from_user
        BOT_ID = await c.get_me()
        if user.id == from_user.id:
            return await message.reply_text(
                "You can't gban yourself !"
            )
        elif user.id == BOT_ID:
            await message.reply_text("ɪ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏsᴇʟғ")
        elif user.id in SUDO_USERS:
            await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ sᴜᴅᴏ ᴜsᴇʀ")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"🚷 **ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴɪɴɢ {user.mention}**\n⏱ ᴇxᴘᴇᴄᴛᴇᴅ ᴛɪᴍᴇ: `{len(served_chats)}`"
            )
            number_of_chats = 0
            for num in served_chats:
                try:
                    await c.ban_chat_member(num, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
🚷 **ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ [{BOT_NAME}](https://t.me/{bn})

**Origin:** {message.chat.title} [`{message.chat.id}`]
**Sudo User:** {from_user.mention}
**Banned User:** {user.mention}
**Banned User ID:** `{user.id}`
**Chats:** `{number_of_chats}`"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    BOT_ID = await c.get_me()
    if user_id == from_user_id:
        await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ")
    elif user_id == BOT_ID:
        await message.reply_text("ɪ ᴄᴀɴ'ᴛ ɢʙᴀɴ ᴍʏsᴇʟғ")
    elif user_id in SUDO_USERS:
        await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ sᴜᴅᴏ ᴜsᴇʀ")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"🚷 **ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴɪɴɢ {mention}**\n⏱ ᴇxᴘᴇᴄᴛᴇᴅ ᴛɪᴍᴇ: `{len(served_chats)}`"
            )
            number_of_chats = 0
            for num in served_chats:
                try:
                    await c.ban_chat_member(num, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
🚷 **ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ [{BOT_NAME}](https://t.me/{bn})

**ᴏʀɪɢɪɴ:** {message.chat.title} [`{message.chat.id}`]
**sᴜᴅᴏ ᴜsᴇʀ:** {from_user_mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ:** {mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ:** `{user_id}`
**ᴄʜᴀᴛs:** `{number_of_chats}`"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@Client.on_message(command(["ungban", f"ungban@{bn}"]) & other_filters)
@bot_creator
async def ungban_global(c: Client, message: Message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**ᴜsᴀɢᴇ:**\n\n/ungban [username | user_id]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await c.get_users(user)
        from_user = message.from_user
        BOT_ID = await c.get_me()
        if user.id == from_user.id:
            await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜɴɢʙᴀɴ ʏᴏᴜʀsᴇʟғ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ")
        elif user.id == BOT_ID:
            await message.reply_text("ɪ ᴄᴀɴ'ᴛ ᴜɴɢʙᴀɴ ᴍʏsᴇʟғ ʙᴇᴄᴀᴜsᴇ ɪ ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ")
        elif user.id in SUDO_USERS:
            await message.reply_text("sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ/ᴜɴɢʙᴀɴɴᴇᴅ")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ᴜɴɢʙᴀɴɴᴇᴅ")
            else:
                await c.unban_chat_member(chat_id, user.id)
                await remove_gban_user(user.id)
                await message.reply_text("✅ ᴛʜɪs ᴜsᴇʀ ʜᴀs ᴜɴɢʙᴀɴɴᴇᴅ")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    BOT_ID = await c.get_me()
    if user_id == from_user_id:
        await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜɴɢʙᴀɴ ʏᴏᴜʀsᴇʟғ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ")
    elif user_id == BOT_ID:
        await message.reply_text(
            "ɪ ᴄᴀɴ'ᴛ ᴜɴɢʙᴀɴ ᴍʏsᴇʟғ ʙᴇᴄᴀᴜsᴇ ɪ ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ"
        )
    elif user_id in SUDO_USERS:
        await message.reply_text("sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ'ᴛ ʙᴇ ɢʙᴀɴɴᴇᴅ/ᴜɴɢʙᴀɴɴᴇᴅ ")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("ᴛʜɪs ᴜsᴇʀ ɴᴏᴛ ɢʙᴀɴɴᴇᴅ")
        else:
            await c.unban_chat_member(chat_id, user_id)
            await remove_gban_user(user_id)
            await message.reply_text("✅ ᴛʜɪs ᴜsᴇʀ ʜᴀs ᴜɴɢʙᴀɴɴᴇᴅ")
