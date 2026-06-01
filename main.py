import os
import re
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp

COOKIES_FILE = None
if os.environ.get("YOUTUBE_COOKIES"):
    import atexit
    _tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    _tmp.write(os.environ["YOUTUBE_COOKIES"])
    _tmp.close()
    COOKIES_FILE = _tmp.name
    atexit.register(os.unlink, COOKIES_FILE)

BOT_TOKEN = os.environ["BOT_TOKEN"]
URL_REGEX = re.compile(r'https?://(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|facebook\.com|fb\.watch)\S+', re.I)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Envie um link do YouTube, Instagram, TikTok ou Facebook para baixar o vídeo.')

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ''
    match = URL_REGEX.search(text)
    if not match:
        return

    url = match.group(0)
    status = await update.message.reply_text('⏳ Baixando...')

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'outtmpl': f'{tmpdir}/video.%(ext)s',
            'format': 'bestvideo[ext=mp4][filesize<50M]+bestaudio[ext=m4a]/best[ext=mp4][filesize<50M]/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            **({"cookiefile": COOKIES_FILE} if COOKIES_FILE else {}),
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info).replace(f'.{info["ext"]}', '.mp4')

            await update.message.reply_video(video=open(filepath, 'rb'), filename='video.mp4')
        except Exception as e:
            print(e)
            await update.message.reply_text('❌ Não foi possível baixar o vídeo. Verifique o link e tente novamente.')
        finally:
            await status.delete()

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
