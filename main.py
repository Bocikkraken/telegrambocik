# main.py
import os
import telebot
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
INFURA_URL = os.getenv("INFURA_URL")

bot = telebot.TeleBot(TOKEN)
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Upewnij się, że połączono z siecią
if not w3.isConnected():
    print("[Błąd] Nie można połączyć się z siecią Ethereum.")
    exit()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Witaj! Wyślij mi adres ETH, a wyślę testową ilość ETH (mainnet). Używaj odpowiedzialnie!")

@bot.message_handler(func=lambda message: True)
def send_eth(message):
    recipient = message.text.strip()

    if not w3.isAddress(recipient):
        bot.reply_to(message, "❌ To nie jest prawidłowy adres Ethereum.")
        return

    try:
        nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)
        tx = {
            'nonce': nonce,
            'to': recipient,
            'value': w3.to_wei(0.0001, 'ether'),  # Możesz zmienić ilość
            'gas': 21000,
            'gasPrice': w3.to_wei('25', 'gwei')
        }

        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_url = f"https://etherscan.io/tx/{tx_hash.hex()}"
        bot.reply_to(message, f"✅ ETH wysłane!
Potwierdzenie: {tx_url}")

    except Exception as e:
        bot.reply_to(message, f"❌ Błąd przy wysyłaniu: {str(e)}")

bot.polling()
