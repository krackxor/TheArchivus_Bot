from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from engine import process_move
from database import get_player

TOKEN = "TOKEN_BOT_TELEGRAM_KAMU_DI_SINI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name

    # Inisialisasi player di database saat pertama kali main
    player = get_player(user_id, username)

    welcome_text = (
        f"📜 **Selamat Datang di The Archivus, {username}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Ketik /move untuk melangkah ke dalam kehampaan.\n"
        "Ketik /status untuk melihat kondisimu."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Memanggil mesin utama The Archivus (Logika 3-15 langkah)
    event_type, event_data, narration = process_move(user_id)

    # Kirim narasi dasar (Sedang berjalan)
    await update.message.reply_text(f"👣 {narration}")

    # Tangani nasib pemain berdasarkan hasil lemparan mesin
    if event_type == "npc_baik" or event_type == "npc_jahat":
        npc_name = event_data["identity"]
        npc_dialog = event_data["dialog"]
        
        text = (
            f"👤 **Seseorang muncul dari balik bayangan!**\n\n"
            f"Kamu bertemu {npc_name}.\n\n"
            f"Dia menatapmu dan berbisik: *\"{npc_dialog}\"*"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    elif event_type == "monster":
        monster_name = event_data["name"]
        text = (
            f"⚔️ **AWAS!**\n"
            f"**{monster_name}** menghadang jalanmu!\n\n"
            f"*(Fitur Battle Puzzle sedang dikembangkan oleh Scriptwriter...)*"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = get_player(user_id)

    text = (
        f"📊 **Buku Catatan {player['username']}**\n"
        f"❤️ HP: {player['hp']}/{player['max_hp']}\n"
        f"🔮 MP: {player['mp']}/{player['max_mp']}\n"
        f"💰 Pecahan Memori (Gold): {player['gold']}\n"
        f"💀 Entitas Terhapus (Kills): {player['kills']}\n"
        f"📍 Tingkat Kewaspadaan: {player['step_counter']}/15"
    )
    await update.message.reply_text(text)

def main():
    # Bangun aplikasi bot
    app = Application.builder().token(TOKEN).build()

    # Daftarkan perintah (Command)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("move", move))
    app.add_handler(CommandHandler("status", status))

    print("👁️ The Archivus telah bangkit. Bot sedang mendengarkan...")

    # Jalankan bot (Bot akan terus menyala sampai kamu matikan terminalnya)
    app.run_polling()

if __name__ == "__main__":
    main()
