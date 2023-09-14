import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext
from tqdm import tqdm

TOKEN = os.getenv('5995368320:AAHhq6gZ0M-EHSfX6w96XXUUN-Z7oSg7S5w')
api_id = '20210345'
api_hash = '11bcb58ae8cfb85168fc1f2f8f4c04c2'

app = Client("my_account", api_id=api_id, api_hash=api_hash)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

resolution = '640x480'  # Default resolution

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a video and I will encode it.')

def set_resolution(update: Update, context: CallbackContext) -> None:
    global resolution
    resolution = context.args[0]
    update.message.reply_text(f'Set resolution to {resolution}.')

@app.on_message(filters.video)
async def encode_video(client: Client, message: Message):
    file_path = await client.download_media(
        message=message,
        progress=progress,
        progress_args=("Downloading", message)
    )

    process = (
        ffmpeg
        .input(file_path)
        .output('output.mp4', vf=f'scale={resolution}', watermark='Anime Compass 🧭')
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    for line in tqdm(iter(process.stderr.readline, b''), desc="Encoding"):
        pass

    await client.send_video(
        chat_id=message.chat.id,
        video='output.mp4',
        progress=progress,
        progress_args=("Uploading", message)
    )

    os.remove(file_path)
    os.remove('output.mp4')

def progress(current: int, total: int, prefix: str, message: Message):
    message.edit_text(f'{prefix}: {current * 100 / total:.1f}%')

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("set_resolution", set_resolution))

app.run()
  
