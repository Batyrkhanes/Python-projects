import requests
from bs4 import BeautifulSoup
import telebot
from googletrans import Translator
translator = Translator()

user_data = {}
bot = telebot.TeleBot("Your token")

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Hello! I'm a bot that helps you find apartments in Kazakhstan. Enter a city, for example: \nalma-ata\natyrau\nastana\nshymkent\nhurbaev (Nurbaev)\nabay (Abay city)\nakm (Akmola city): ")
    
@bot.message_handler(func=lambda msg: msg.chat.id in user_data and 'city' not in user_data[msg.chat.id])
def get_city(message):
    city = message.text.lower().replace(" ", "-")
    user_data[message.chat.id]["city"] = city
    bot.send_message(message.chat.id, "How many rooms (1,2,3,4,5): ")


@bot.message_handler(func=lambda msg: msg.chat.id in user_data and 'rooms' not in user_data[msg.chat.id])
def get_rooms(message):
    rooms = message.text.strip()
    user_data[message.chat.id]["rooms"] = rooms

    city = user_data[message.chat.id]["city"]
    url = f"https://www.olx.kz/nedvizhimost/prodazha-kvartiry/{city}/?search[filter_enum_kolichestvo-komnat][0]={rooms}"


    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("div[data-testid='l-card']")

    count = 0
    if not cards:
        bot.send_message(message.chat.id, "Unfortunately, nothing was found. Try changing the city or number of rooms.")
        return


    bot.send_message(message.chat.id, " 🔍 Searching for apartments with your filters")
    for card in cards:
      title = card.select_one("h4")
      price = card.select_one("p[data-testid='ad-price']")

      if title and price:
          title_text = title.text.strip()
          price_text = price.text.strip()

          if "договор" in price_text.lower():
              continue

          try:
              translated_title = translator.translate(title_text, src='auto', dest='en').text
          except Exception:
              translated_title = title_text + " (translation failed)"

          bot.send_message(message.chat.id, f"Title: {translated_title}\nPrice: {price_text} (tenge)")

          count += 1
      if count >= 8:
          break



    bot.send_message(message.chat.id, f"✅ Done! Type /start to try again. Thank you for using the bot!")
    user_data.pop(message.chat.id)

bot.polling()
