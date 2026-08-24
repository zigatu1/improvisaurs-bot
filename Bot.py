import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import os

# ==========================================
# 🛠 НАСТРОЙКИ БОТА И БАЗА FILE_ID
# ==========================================

# Токен берется из переменных окружения Bothost
TOKEN = os.getenv('Token')
ADMIN_USERNAME = 'zigatul'

TRACKS = {
    "1": {"name": "1. Парк Юрского периода", "file_id": "CQACAgIAAxkBAAM3aogU5cCGjZNAoeBVCRk0i9jVtQkAAhSnAAIGXkBIep9i7AAB9nblPQQ"},
    "2": {"name": "2. Звездные войны", "file_id": "CQACAgIAAxkBAAM7aogVnQ0-wQ3NLX5xi5nr4vz1A3kAAh6nAAIGXkBITcELPhfYqrQ9BA"},
    "3": {"name": "3. Матрица", "file_id": "CQACAgIAAxkBAAM5aogVV5RxUllNO6phJOc4EscYa_UAAhqnAAIGXkBI2hphUEMEfdk9BA"},
    "4": {"name": "4. Властелин колец", "file_id": "CQACAgIAAxkBAANBaogWMaAJKyI2Tn_AwneJzc_K4OcAAianAAIGXkBIBJ8Me6VpQXg9BA"},
    "5": {"name": "5. Терминатор 2", "file_id": "CQACAgIAAxkBAAM9aogV19ez4iI06DbpvMB5OuhbTWIAAiOnAAIGXkBIHLnWzpmE3rY9BA"},
    "6": {"name": "6. Интерстеллар", "file_id": "CQACAgIAAxkBAAM9aogV19ez4iI06DbpvMB5OuhbTWIAAiOnAAIGXkBIHLnWzpmE3rY9BA"},
    "7": {"name": "7. Пираты Карибского моря", "file_id": "CQACAgIAAxkBAANFaogWdlu2HfOcORAzhf_GjJSWPBUAAi2nAAIGXkBIxLr9G-DgLWg9BA"},
    "8": {"name": "8. Титаник", "file_id": "CQACAgIAAxkBAANHaogWrY9OVgoZhcI0CcIw2Nmkme8AAi-nAAIGXkBIMD86wSl_8-k9BA"},
    "9": {"name": "9. Сияние", "file_id": "CQACAgIAAxkBAANJaogWvPUWM-RGvjyEbdLEOq0sxikAAjGnAAIGXkBIQCfkJTsbCnw9BA"},
    "10": {"name": "10. Охотники за привидениями", "file_id": "CQACAgIAAxkBAANLaogW8Sh2YZKiIU86FJz50br4iZEAAjKnAAIGXkBIgEJkQiUVUwQ9BA"}
}

# Текст правил, разбитый на страницы
RULES = [
    "**Добро пожаловать в мир Импровизавров!** 🦖\n\nДобро пожаловать в мир, где вы становитесь режиссёрами самых абсурдных, смешных и непредсказуемых фильмов! Ваша задача — создать шедевр с динозавром в главной роли и сорвать овации зрителей.",
    "🎬 **1. Мотор! Подготовка к съемкам**\n\nВ начале партии каждый игрок придумывает название для своей киностудии и торжественно представляет её остальным участникам.\nЗатем каждый участник получает на руку 6 базовых карт Сцен.\nВ центр стола в открытую выкладываются две общие карты: они задают 1-й (завязка) и 5-й (финал) кадры будущего фильма.\n\nНа этап «написания сценария» даётся ровно 3 минуты. За это время игроки выбирают из своей руки 3 карты, которые свяжут историю воедино, и выкладывают их перед собой рубашкой вверх.",
    "🎥 **2. Камера! Питчинг и Логлайн**\n\nУчастники по очереди презентуют (питчат) свои фильмы. Во время своего выступления игрок раскрывает выбранные 3 карты, по одной выкладывая их между 1-м и 5-м кадрами на столе, параллельно эмоционально рассказывая сюжет.\n\nПосле выступления игрок забирает эти 3 карты и оставляет их лежать перед собой в открытую, чтобы все зрители помнили, о чём был этот шедевр.\nКогда все выступили, объявляется раунд «Логлайна»: каждый игрок должен описать концепцию своего фильма ровно в одно ёмкое предложение.",
    "🏆 **3. Снято! Голосование и Награждение**\n\nНаступает время кинопремий! Для голосования каждый берёт по 1 монете (ДиноОскару) в каждую руку.\nНа счёт «три» все игроки одновременно отдают монеты чужим киностудиям. Вы можете отдать обе монеты одному, самому гениальному фильму, или распределить их между двумя разными.\n\nВ конце раунда все раскрытые карты (включая 1-й и 5-й кадры со стола) отправляются в сброс. Игроки добирают на руку новые карты, чтобы их снова стало 6.",
    "🎭 **4. Режиссёрские испытания: Киномеханики и Твисты**\n\nКогда базовые правила освоены, добавьте в игру усложнения:\n\n• **Киномеханики:** Выдаются по 2 на руку (после базовой раздачи). Одну из них можно в закрытую подкинуть случайному оппоненту. Карта вскрывается до начала питчинга жертвы. Условия (например, использовать определённую букву или саундтрек) задаёт тот, кто её подкинул.\n\n• **Твисты:** Добавляются в игру позже, раздаются по 2 на руку. За раунд можно подкинуть только 1 твист. Он вскрывается сразу после питчинга оппонента, заставляя его на ходу придумывать абсолютно новую концовку своего фильма!",
    "🏁 **Конец игры**\n\nПартия продолжается, пока не иссякнет колода или пока режиссёрам не надоест творить (в среднем от 40 до 120 минут). Побеждает киностудия, собравшая наибольшее количество монет! \n\nПобедитель произносит торжественную благодарственную речь. 🍿"
]

# ==========================================
# 🚀 ОСНОВНОЙ КОД
# ==========================================

bot = telebot.TeleBot(TOKEN)
user_state = {}

def init_db():
    conn = sqlite3.connect('improvisaurs_users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()

init_db()

def clean_chat(chat_id, msg_type):
    if chat_id in user_state and msg_type in user_state[chat_id]:
        try:
            bot.delete_message(chat_id, user_state[chat_id][msg_type])
        except:
            pass

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    
    conn = sqlite3.connect('improvisaurs_users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, username, first_name) VALUES (?, ?, ?)", 
                   (message.from_user.id, message.from_user.username, message.from_user.first_name))
    conn.commit()
    conn.close()

    try: bot.delete_message(chat_id, message.message_id)
    except: pass

    # Обновленное меню с кнопкой Правил
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(KeyboardButton("📜 Правила игры"), KeyboardButton("🎵 Саундтреки"))
    markup.add(KeyboardButton("🎭 Жанры"), KeyboardButton("🌐 Сайт"))
    markup.add(KeyboardButton("✍️ Оставить отзыв"))
    
    clean_chat(chat_id, 'static_menu')
    msg_static = bot.send_message(chat_id, "🎬 Главное меню:", reply_markup=markup)
    
    clean_chat(chat_id, 'dynamic')
    msg = bot.send_message(chat_id, "Добро пожаловать на съемочную площадку Импровизавров! Выбирай действие ниже 👇")
    
    if chat_id not in user_state: user_state[chat_id] = {}
    user_state[chat_id]['static_menu'] = msg_static.message_id
    user_state[chat_id]['dynamic'] = msg.message_id

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    
    # ИСПРАВЛЕНИЕ 1: Инициализируем словарь состояния для пользователя, если его нет
    if chat_id not in user_state:
        user_state[chat_id] = {}
        
    try: bot.delete_message(chat_id, message.message_id)
    except: pass

    if message.text == "📜 Правила игры":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Далее ➡️", callback_data="rule_1"))
        
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, RULES[0], reply_markup=markup, parse_mode="Markdown")
        user_state[chat_id]['dynamic'] = msg.message_id

    elif message.text == "🎭 Жанры":
        genres_text = (
            "🎥 **10 жанров для твоего блокбастера:**\n\n"
            "1. Ужасы\n2. Комедия\n3. Мюзикл\n4. Киберпанк\n5. Вестерн\n"
            "6. Нуар-детектив\n7. Мелодрама\n8. Фэнтези\n9. Постапокалипсис\n10. Боевик"
        )
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, genres_text, parse_mode="Markdown")
        user_state[chat_id]['dynamic'] = msg.message_id
        
    elif message.text == "🎵 Саундтреки":
        markup = InlineKeyboardMarkup(row_width=1)
        for key, info in TRACKS.items():
            markup.add(InlineKeyboardButton(info["name"], callback_data=f"snd_{key}"))
        
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, "Выбирай атмосферу для своей сцены:", reply_markup=markup)
        user_state[chat_id]['dynamic'] = msg.message_id
        
    elif message.text == "🌐 Сайт":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Перейти на improvisaurs.ru", url="https://improvisaurs.ru/"))
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, "Жми на кнопку ниже, чтобы перейти на наш сайт 🦖", reply_markup=markup)
        user_state[chat_id]['dynamic'] = msg.message_id
        
    elif message.text == "✍️ Оставить отзыв":
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, "Оставить отзыв, поделиться идеей или задать вопрос можно напрямую создателю игры:\n👉 **@zigatul**", parse_mode="Markdown")
        user_state[chat_id]['dynamic'] = msg.message_id
        
    else:
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, "Я понимаю только команды из меню! Пожалуйста, воспользуйся кнопками ниже 👇")
        user_state[chat_id]['dynamic'] = msg.message_id

# Обработка кнопок перелистывания правил
@bot.callback_query_handler(func=lambda call: call.data.startswith('rule_'))
def rule_pagination(call):
    bot.answer_callback_query(call.id)
    page = int(call.data.split('_')[1])
    
    markup = InlineKeyboardMarkup()
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"rule_{page-1}"))
    if page < len(RULES) - 1:
        buttons.append(InlineKeyboardButton("Далее ➡️", callback_data=f"rule_{page+1}"))
    
    if buttons:
        markup.row(*buttons)
        
    bot.edit_message_text(RULES[page], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('snd_'))
def send_audio_track(call):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)
    track_key = call.data.split('snd_')[1]
    file_id = TRACKS[track_key]["file_id"]
    
    # ИСПРАВЛЕНИЕ 2: Инициализируем словарь до блока try/except
    if chat_id not in user_state:
        user_state[chat_id] = {}
        
    clean_chat(chat_id, 'audio')
    
    try:
        audio_msg = bot.send_audio(chat_id, file_id)
        user_state[chat_id]['audio'] = audio_msg.message_id
    except:
        clean_chat(chat_id, 'dynamic')
        msg = bot.send_message(chat_id, "Трек пока не загружен! Ждем обновления базы.")
        user_state[chat_id]['dynamic'] = msg.message_id

# Убрали сбор медиа-отзывов. Теперь просто удаляем спам. Оставили функцию ID только для админа
@bot.message_handler(content_types=['audio', 'voice', 'document', 'photo', 'video', 'video_note', 'sticker'])
def get_file_id(message):
    if message.from_user.username == ADMIN_USERNAME:
        if message.audio: bot.reply_to(message, f"`{message.audio.file_id}`", parse_mode="Markdown")
        elif message.voice: bot.reply_to(message, f"`{message.voice.file_id}`", parse_mode="Markdown")
    else:
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass

bot.polling(none_stop=True)