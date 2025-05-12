from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pydub import AudioSegment
import os

# Tokeni buraya əlavə et
TOKEN = "YOUR_NEW_BOT_TOKEN"

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.audio or update.message.voice:
        # Faylı yüklə
        file = await update.message.effective_attachment.get_file()
        input_path = "input.mp3"
        output_path = "output.mp3"

        await file.download_to_drive(input_path)

        # Səsə bass əlavə et
        sound = AudioSegment.from_file(input_path)
        boosted = sound.low_pass_filter(150) + 6
        boosted.export(output_path, format="mp3")

        # Geri göndər
        await update.message.reply_audio(audio=open(output_path, "rb"))

        # Faylları təmizlə
        os.remove(input_path)
        os.remove(output_path)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
app.run_polling()
