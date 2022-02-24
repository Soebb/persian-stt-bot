import os
from transcribe_anything.api import transcribe
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = ""
API_ID = ""
API_HASH = ""

Bot = Client(
    "Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, I'm Persian transcriber Bot.

Send a media(video/audio) or a YouTube URL or path of a local file in your system.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb/persian-transcriber-bot'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.text)
async def from_yturl_or_local_file(_, m):
    output_name = f"transcript{m.message_id}.txt"
    await m.reply("Processing..")
    transcribe(m.text, output_name)
    await m.reply_document(output_name)


@Bot.on_message(filters.private & filters.media)
async def from_tg_files(_, m):
    msg = await m.reply("Downloading..")
    media = await m.download()
    await msg.edit("Processing..")
    output_name = media.rsplit('.', 1)[0] + ".txt"
    transcribe(media, output_name)
    await m.reply_document(output_name)


Bot.run()
