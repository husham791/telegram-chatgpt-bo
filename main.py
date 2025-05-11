import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

openai.api_key = os.getenv("OPENAI_API_KEY")

def start(update, context):
    update.message.reply_text("أهلاً! أرسل لي أي رسالة وسأرد عليك باستخدام ChatGPT.")

def handle_message(update, context):
    user_message = update.message.text
    try:
        # إرسال الرسالة إلى OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        # استخراج الرد من OpenAI
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        # فحص إذا كان السبب هو انتهاء الرصيد
        error_message = str(e).lower()
        if "quota" in error_message:
            # إذا انتهى الرصيد
            reply = "⚠️ عذرًا، انتهى رصيد البوت في OpenAI حاليًا. يرجى المحاولة لاحقًا."
        else:
            # إذا كان الخطأ من نوع آخر
            reply = f"❌ حدث خطأ أثناء الاتصال بـ OpenAI. الرسالة: {str(e)}"
    
    # إرسال الرد للمستخدم
    update.message.reply_text(reply)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
