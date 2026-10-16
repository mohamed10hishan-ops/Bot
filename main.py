from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import sqlite3, os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running ✅'

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TOKEN = os.environ.get('TOKEN', '8610523381:AAH5bL7jBp9KEP6i5JkOuFjAdx7zZQE3CtY')
conn = sqlite3.connect('creds.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS creds (email TEXT, password TEXT)')
conn.commit()

async def start(u, c):
    await u.message.reply_text('أرسل: email password')

async def save(u, c):
    p = u.message.text.split()
    if len(p) == 2:
        conn.execute('INSERT INTO creds VALUES (?,?)', p)
        conn.commit()
        await u.message.reply_text('✅ تم الحفظ')

async def show(u, c):
    r = conn.execute('SELECT * FROM creds').fetchall()
    await u.message.reply_text('\n'.join(f'{e}:{p}' for e, p in r) or 'فاضي')

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('list', show))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save))
    application.run_polling()