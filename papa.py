# Importing the required libraries
import os
import telebot
from PIL import Image, ImageDraw, ImageFont
from telethon import TelegramClient

# Setting the bot token, API ID, API hash and watermark text
TOKEN = "6591286139:AAFQCCfj7uQ5Lp0beXBmNPjm26VABvCVHJ4"
API_ID = "20210345"
API_HASH = "11bcb58ae8cfb85168fc1f2f8f4c04c2"
WATERMARK = "Anime Compass 🧭"

# Creating a telebot instance
bot = telebot.TeleBot(TOKEN)

# Creating a TelegramClient instance
client = TelegramClient("bot", API_ID, API_HASH)

# Defining a function to add watermark to an image
def add_watermark(image):
  # Opening the image and getting its size
  im = Image.open(image)
  width, height = im.size

  # Creating a new image object with the same mode and size as the original image
  new_im = Image.new(im.mode, (width, height))

  # Drawing the watermark text on the new image object
  draw = ImageDraw.Draw(new_im)
  font = ImageFont.truetype("arial.ttf", 32) # You can change the font and size here
  text_width, text_height = draw.textsize(WATERMARK, font)
  x = width - text_width - 10 # You can change the margin here
  y = 10 # You can change the margin here
  draw.text((x, y), WATERMARK, font=font, fill=(255, 255, 255)) # You can change the color here

  # Pasting the new image object over the original image
  im.paste(new_im, (0, 0), new_im)

  # Saving the modified image
  im.save(image)

# Defining a handler for photo messages
@bot.message_handler(content_types=["photo"])
def photo_handler(message):
  # Getting the file ID and file path of the photo message
  file_id = message.photo[-1].file_id
  file_path = bot.get_file(file_id).file_path

  # Downloading the photo to a local file using Telethon client
  file_name = file_path.split("/")[-1]
  client.download_media(file_id, file_name)

  # Adding watermark to the photo
  add_watermark(file_name)

  # Sending the modified photo back to the user using Telethon client
  client.send_file(message.chat.id, file_name)

  # Deleting the local file
  os.remove(file_name)

# Polling for updates using Telebot instance
bot.polling()

