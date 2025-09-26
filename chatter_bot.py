import logging
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

# 🔑 Telegram Bot Token и Channel ID
BOT_TOKEN = "8187567616:AAG_1VuKg5W_fQgAfZHOSMDxxHTzr105Das"
CHANNEL_ID = "-1002756706595"
ADMIN_ID = 7085368976  # <-- твой Telegram ID

# 🔑 Google Sheets Setup через Render Env Var GOOGLE_CREDS
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_CREDS")  # JSON берём из переменной окружения Render
if not creds_json:
    raise Exception("❌ GOOGLE_CREDS переменная окружения не найдена!")

creds_dict = json.loads(creds_json)
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(CREDS)
sheet = client.open("Onlycats Applications").sheet1

# 📝 Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🗂️ Состояния анкеты
(Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12) = range(12)

# 🚀 Старт анкеты
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как к тебе обращаться?")
    return Q1

async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Твой возраст?")
    return Q2

async def q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("В какой стране проживаешь?")
    return Q3

async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    await update.message.reply_text("Какой у тебя опыт на OnlyFans?")
    return Q4

async def q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["of_experience"] = update.message.text
    keyboard = [["Утро (08–16)", "Вечер (16–00)", "Ночь (00–08)"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("В какую смену работаешь?", reply_markup=reply_markup)
    return Q5

async def q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["shift"] = update.message.text
    await update.message.reply_text(
        "Где работал(а), сколько времени, какие были результаты и почему ушёл(ушла)?",
        reply_markup=ReplyKeyboardRemove()
    )
    return Q6

async def q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["previous"] = update.message.text
    keyboard = [["A1", "A2", "B1"], ["B2", "C1", "C2"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Какой у тебя уровень английского языка?", reply_markup=reply_markup)
    return Q7

async def q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["english"] = update.message.text
    await update.message.reply_text("Фанат пишет: “I can find free stuff online. Why should I pay you?” — твой ответ?",
                                    reply_markup=ReplyKeyboardRemove())
    return Q8

async def q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q8"] = update.message.text
    await update.message.reply_text("Фанат пишет: “Babe, I can't play right now, I'm at work!” — твой ответ?")
    return Q9

async def q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q9"] = update.message.text
    await update.message.reply_text("Фанат пишет: “$40 за видео — дорого.” — твой ответ?")
    return Q10

async def q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q10"] = update.message.text
    await update.message.reply_text("Фанат пишет: “I don’t have much money, but I’m so horny rn.” — твой ответ?")
    return Q11

async def q11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q11"] = update.message.text
    await update.message.reply_text(
        "На модель подписался новый фан. Что ты напишешь ему в первые минуты? "
        "Через какое время и какие шаги предпримешь, чтобы вывести его в живой диалог и подвести к продажам?"
    )
    return Q12

async def q12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q12"] = update.message.text

    username = update.message.from_user.username or "(no username)"
    user_id = update.message.from_user.id

    result_message = (
        f"🧾 Новая анкета:\n"
        f"👤 Username: @{username}\n"
        f"🆔 ID: {user_id}\n"
        f"📛 Имя: {context.user_data['name']}\n"
        f"🎂 Возраст: {context.user_data['age']}\n"
        f"🌍 Страна: {context.user_data['country']}\n"
        f"📈 Опыт на OF: {context.user_data['of_experience']}\n"
        f"🕐 Смена: {context.user_data['shift']}\n"
        f"💼 Предыдущий опыт: {context.user_data['previous']}\n"
        f"📚 Английский: {context.user_data['english']}\n\n"
        f"❓ Q1: {context.user_data['q8']}\n"
        f"❓ Q2: {context.user_data['q9']}\n"
        f"❓ Q3: {context.user_data['q10']}\n"
        f"❓ Q4: {context.user_data['q11']}\n"
        f"❓ Q5: {context.user_data['q12']}"
    )

    await context.bot.send_message(chat_id=CHANNEL_ID, text=result_message)

    # Сохраняем в Google Sheets
    sheet.append_row([
        username, str(user_id),
        context.user_data["name"],
        context.user_data["age"],
        context.user_data["country"],
        context.user_data["of_experience"],
        context.user_data["shift"],
        context.user_data["previous"],
        context.user_data["english"],
        context.user_data["q8"],
        context.user_data["q9"],
        context.user_data["q10"],
        context.user_data["q11"],
        context.user_data["q12"]
    ])

    await update.message.reply_text("Спасибо за заявку, анкета отправлена.")
    return ConversationHandler.END

# ❌ Отмена анкеты
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анкета отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# 📢 Команда рассылки
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У тебя нет прав для рассылки.")
        return

    if not context.args:
        await update.message.reply_text("Используй так: /broadcast текст сообщения")
        return

    text_to_send = " ".join(context.args)
    users = sheet.col_values(2)  # колонка user_id
    sent, failed = 0, 0

    for user_id in users[1:]:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=text_to_send)
            sent += 1
        except Exception as e:
            failed += 1
            logger.error(f"Ошибка при отправке {user_id}: {e}")

    await update.message.reply_text(f"✅ Рассылка завершена.\nОтправлено: {sent}\nОшибок: {failed}")

# ▶️ Main
if __name__ == "__main__":
    print("🚀 Бот запущен и работает...")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, q1)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, q3)],
            Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, q4)],
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, q5)],
            Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, q6)],
            Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, q7)],
            Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, q8)],
            Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, q9)],
            Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, q10)],
            Q11: [MessageHandler(filters.TEXT & ~filters.COMMAND, q11)],
            Q12: [MessageHandler(filters.TEXT & ~filters.COMMAND, q12)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()