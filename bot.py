import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаём клавиатуру с кнопкой
    keyboard = [
        [InlineKeyboardButton("Получить расписание", callback_data="get_schedule")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с кнопкой
    await update.message.reply_text(
        "Привет! Я ваш ЯКОВ.\nНажмите кнопку ниже, чтобы получить расписание:",
        reply_markup=reply_markup
    )

# Обработчик нажатия кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие кнопки
    
    if query.data == "get_schedule":
        pdf_url = "http://www.prk.kuzstu.ru/upload/iblock/091/ahmv6uu8lzzd51l371fvleesyeiaeuen/%D0%A1%D0%9F%D0%9E,%20%D0%9B%D0%B8%D1%86%D0%B5%D0%B9%20%20%D0%A0%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20%2013.01.2025-19.01.2025%20%D1%87%D0%B5%D1%82%D0%BD%D0%B0%D1%8F%20%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8F.pdf"
        local_filename = "расписание.pdf"
        
        try:
            # Скачиваем файл
            response = requests.get(pdf_url)
            response.raise_for_status()  # Проверка статуса HTTP
            with open(local_filename, "wb") as pdf_file:
                pdf_file.write(response.content)
            print("Файл успешно скачан:", local_filename)
            
            # Отправляем файл пользователю
            await query.message.reply_document(document=open(local_filename, "rb"))
            print("Файл отправлен пользователю.")
            
        except requests.exceptions.RequestException as e:
            # Ошибка загрузки файла
            await query.message.reply_text("Не удалось скачать файл. Проверьте URL.")
            print(f"Ошибка загрузки: {e}")
            
        except Exception as e:
            # Общие ошибки
            await query.message.reply_text("Произошла ошибка при обработке файла.")
            print(f"Ошибка: {e}")
            
        finally:
            # Удаляем файл, если он был создан
            if os.path.exists(local_filename):
                os.remove(local_filename)
                print("Локальный файл удален.")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я могу помочь вам узнать расписание занятий.\n"
        "Команды:\n/start - Начать\n/help - Справка\n/mironov - Скачать расписание"
    )

# Главная функция
def main():
    print("Бот запущен и готов к работе.")
    # Укажите ваш токен
    TOKEN = "7775696391:AAHO6nal2uBIpE2TuQbKo9wc7DPxB6Fw4Bg"

    # Создание приложения
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавление команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))  # Обработчик кнопки

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
