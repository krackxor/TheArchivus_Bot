from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from engine import process_move
from database import get_player, auto_seed_content

TOKEN = "TOKEN_BOT_MU_DI_SINI"

def get_nav_keyboard():
    """Membuat susunan tombol yang terorganisir untuk navigasi."""
    keyboard = [
        [InlineKeyboardButton("Utara ⬆️", callback_data="move_utara")],
        [InlineKeyboardButton("Barat ⬅️", callback_data="move_barat"), InlineKeyboardButton("Timur ➡️", callback_data="move_timur")],
        [InlineKeyboardButton("Selatan ⬇️", callback_data="move_selatan")],
        [InlineKeyboardButton("📊 Cek Status", callback_data="check_status")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    get_player(user_id, username)

    welcome_text = (
        f"📜 **Selamat Datang di The Archivus, {username}.**\n\n"
        "Dunia ini telah kehilangan ceritanya. Kamu adalah seorang Weaver, "
        "satu-satunya yang bisa menyusun kembali realita lewat kata-kata.\n\n"
        "Pilih arah jalanmu untuk mulai menjelajah."
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=get_nav_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    
    user_id = query.from_user.id
    data = query.data

    if data == "check_status":
        player = get_player(user_id)
        status_text = (
            f"📊 **Catatan {player['username']}**\n"
            f"❤️ HP: {player['hp']}/{player['max_hp']} | 🔮 MP: {player['mp']}/{player['max_mp']}\n"
            f"💰 Gold: {player['gold']} | 💀 Kills: {player['kills']}\n"
            f"📍 Kewaspadaan: {player['step_counter']}/15"
        )
        await query.message.reply_text(status_text, reply_markup=get_nav_keyboard())
        return

    if data.startswith("move_"):
        arah = data.split("_")[1].capitalize()
        
        # Proses mesin logika
        event_type, event_data, narration = process_move(user_id)
        
        await query.edit_message_text(f"👣 Kamu berjalan ke {arah}.\n{narration}")

        if event_type in ["npc_baik", "npc_jahat"]:
            npc_name = event_data["identity"]
            npc_dialog = event_data["dialog"]
            text = (
                f"👤 **Seseorang muncul!**\n\n"
                f"Kamu bertemu {npc_name}.\n"
                f"Dia berbisik: *\"{npc_dialog}\"*"
            )
            await query.message.reply_text(text, parse_mode='Markdown', reply_markup=get_nav_keyboard())
            
        elif event_type == "monster":
            monster_name = event_data["name"]
            text = f"⚔️ **AWAS!**\n**{monster_name}** menghadang jalanmu!"
            await query.message.reply_text(text, parse_mode='Markdown', reply_markup=get_nav_keyboard())
            
        else:
            # Aman, tampilkan tombol jalan lagi
            await query.message.reply_text("Area ini terasa kosong. Ke mana selanjutnya?", reply_markup=get_nav_keyboard())

def main():
    # 1. Jalankan pengecekan dan suntik database
    auto_seed_content()

    # 2. Bangun bot
    app = Application.builder().token(TOKEN).build()

    # 3. Daftarkan handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("👁️ The Archivus telah bangkit. Bot sedang mendengarkan...")
    app.run_polling()

if __name__ == "__main__":
    main()
