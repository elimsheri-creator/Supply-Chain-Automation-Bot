import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Настройка Google Таблиц
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Warehouse_Inventory").sheet1

# 2. Настройка Бота
bot = telebot.TeleBot('8027300175:AAFLU7nFPZMjFlCTjW9EEpUFmnvXI1o_qhs')

# Команда для проверки остатков
@bot.message_handler(commands=['stock'])
def show_stock(message):
    data = sheet.get_all_records()
    text = "📊 Актуальные остатки:\n"
    for row in data:
        text += f"🔹 {row['Толщина']}: {row['Количество']} шт.\n"
    bot.reply_to(message, text)

# Логика проверки размеров
@bot.message_handler(func=lambda message: True)
def check_logic(message):
    try:
        parts = message.text.split()
        w = float(parts[0])
        h = float(parts[1])
        
        # Наша проверка на Oversize
        if (w > 88 and w > 126) or (h > 88 and h > 126):
            res = f"❌ OVERSIZE! Лист {w}x{h} не влезет."
        else:
            res = f"✅ OK. Площадь: {round((w*h)/144, 2)} sq.ft"
        bot.reply_to(message, res)
    except:
        bot.reply_to(message, "Напиши размеры через пробел (напр. 40 150) или жми /stock")

print("Бот вышел на смену! Проверяй в Telegram.")
bot.infinity_polling()