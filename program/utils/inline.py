""" inline section button """

from pyrogram.types import (
  CallbackQuery,
  InlineKeyboardButton,
  InlineKeyboardMarkup,
  Message,
)


def stream_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data=f'stream_menu_panel | {user_id}'),
      InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data=f'set_close'),
    ],
  ]
  return buttons


def menu_markup(user_id):
  buttons = [
    [
      InlineKeyboardButton(text="⏹ sᴛᴏᴘ", callback_data=f'set_stop | {user_id}'),
      InlineKeyboardButton(text="⏸ ᴘᴀᴜsᴇ", callback_data=f'set_pause | {user_id}'),
      InlineKeyboardButton(text="▶️ ʀᴇsᴜᴍᴇ", callback_data=f'set_resume | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔇 ᴍᴜᴛᴇ", callback_data=f'set_mute | {user_id}'),
      InlineKeyboardButton(text="🔊ᴜɴᴍᴜᴛᴇ", callback_data=f'set_unmute | {user_id}'),
    ],
    [
      InlineKeyboardButton(text="🔙 ɢᴏ ʙᴀᴄᴋ", callback_data='stream_home_panel'),
    ]
  ]
  return buttons


close_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "ᴄʟᴏsᴇ", callback_data="set_close"
      )
    ]
  ]
)


back_mark = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        "🔙 ɢᴏ ʙᴀᴄᴋ", callback_data="stream_menu_panel"
      )
    ]
  ]
)
