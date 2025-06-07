from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Fejkowe hashe transakcji (losowo wybierane do symulacji)
FAKE_TX_HASHES = [
    "0x9c1234faab34cd5678e9001def1234567890abcdef1234567890abcdef123456",
    "0x8a5678ddffac12aa7890bbcdef4567890abcdef1234567890abcdef12345678",
    "0xf0abcde34567c89dfd234ef1234567890abcdef1234567890abcdef123456ff",
    "0xab12345cd67890efab1234567890abcdef1234567890abcdef1234567890ab12"
]

# === UWAGA ===
# Wklej tu swój token z BotFather
TOKEN = "TU_WSTAW_SWÓJ_BOT_TOKEN"

# Komenda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Witaj! Podaj adres ETH, a wyślę Ci *fejkowe* 0.0001 ETH i potwierdzenie transakcji. 😄",
        parse_mode="Markdown"
    )

# Obsługa wiadomości (adresów ETH)
async def fake_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()

    if address.startswith("0x") and len(address) == 42:
        fake_tx = random.choice(FAKE_TX_HASHES)
        fake_url = f"https://etherscan.io/tx/{fake_tx}"

        confirmation = (
            "✅ *Transakcja ETH wysłana!*\n\n"
            "📤 Kwota: *0.0001 ETH*\n"
            "🔄 Status: *Zakończona*\n"
            f"🔗 Potwierdzenie (fejk): [etherscan.io]({fake_url})"
        )

        await update.message.reply_text(confirmation, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ To nie wygląda na poprawny adres ETH. Spróbuj ponownie.")

# Główna funkcja bota
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fake_send))

    print("🤖 Fake ETH bot działa!")
    app.run_polling()

