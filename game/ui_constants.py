# game/ui_constants.py

"""
UI CONSTANTS - The Archivus
Standarisasi ikon, warna, dan template text untuk konsistensi UI
"""

# ============================================================================
# IKON SISTEM (Gunakan yang sama di seluruh game)
# ============================================================================

class Icon:
    # Status & Atribut
    HP = "❤️"
    MP = "💧"
    ENERGY = "⚡"
    EXP = "✨"
    LEVEL = "🎖️"
    GOLD = "💰"
    
    # Combat
    ATTACK = "⚔️"
    DEFENSE = "🛡️"
    MAGIC = "🔮"
    SPEED = "💨"
    DODGE = "🌀"
    SKILL = "✨"
    
    # Items & Inventory
    BAG = "🎒"
    POTION = "🧪"
    FOOD = "🍖"
    GEAR = "⚙️"
    WEAPON = "⚔️"
    ARMOR = "🛡️"
    LOOT = "🎁"
    
    # Actions
    MOVE = "🚶"
    RUN = "🏃"
    REST = "🧘"
    REPAIR = "🔨"
    SHOP = "🏪"
    
    # Status Effects
    POISON = "☠️"
    FREEZE = "❄️"
    BURN = "🔥"
    BUFF = "✨"
    DEBUFF = "💀"
    
    # Quest & Progress
    QUEST = "📋"
    COMPLETE = "✅"
    REWARD = "🎁"
    STAR = "⭐"
    
    # Environment
    SAFE = "🌿"
    DANGER = "⚠️"
    BOSS = "👹"
    NPC = "👤"
    LOCATION = "📍"
    
    # UI Elements
    ARROW_UP = "⬆️"
    ARROW_DOWN = "⬇️"
    ARROW_LEFT = "⬅️"
    ARROW_RIGHT = "➡️"
    CLOSE = "❌"
    BACK = "⬅️"
    INFO = "ℹ️"
    
    # Special
    DEATH = "💀"
    WIN = "🎉"
    COMBO = "🔥"


# ============================================================================
# TEMPLATE TEXT (Konsisten & Ringkas)
# ============================================================================

class Text:
    # Separator
    LINE = "━━━━━━━━━━━━━━━━━━━━"
    LINE_SHORT = "━━━━━━━━━━━━━━"
    
    # Common Messages
    NOT_ENOUGH_GOLD = "❌ Emas tidak cukup!"
    NOT_ENOUGH_MP = "❌ MP tidak cukup!"
    NOT_ENOUGH_ENERGY = "❌ Energi habis!"
    ITEM_NOT_FOUND = "❌ Item tidak ditemukan!"
    BAG_EMPTY = "📭 Tas kosong"
    
    # Combat Messages
    PLAYER_WIN = "🎉 MENANG!"
    PLAYER_LOSE = "💀 KALAH"
    ESCAPE_SUCCESS = "🏃 Kabur berhasil!"
    ESCAPE_FAIL = "❌ Gagal kabur!"
    
    # System Messages
    SAVED = "💾 Tersimpan"
    LOADING = "⏳ Memuat..."
    ERROR = "⚠️ Terjadi kesalahan"


# ============================================================================
# LAYOUT HELPERS (Untuk Mobile)
# ============================================================================

class Layout:
    # Max width untuk mobile (karakter)
    MAX_WIDTH = 38
    
    # Spacing
    PADDING_SMALL = "\n"
    PADDING_MEDIUM = "\n\n"
    PADDING_LARGE = "\n\n\n"
    
    @staticmethod
    def header(title):
        """Membuat header yang rapi"""
        return f"{Text.LINE}\n{title}\n{Text.LINE}"
    
    @staticmethod
    def section(title, content):
        """Membuat section dengan title"""
        return f"**{title}**\n{content}"
    
    @staticmethod
    def stat_line(label, value, icon=""):
        """Format: Icon Label: Value"""
        return f"{icon} {label}: `{value}`"


# ============================================================================
# WARNA BAR (Progress Indicators)
# ============================================================================

class BarColor:
    # HP Bar
    HP_HIGH = "🟩"  # > 60%
    HP_MID = "🟨"   # 20-60%
    HP_LOW = "🟥"   # < 20%
    
    # MP Bar
    MP = "🟦"
    
    # Energy Bar
    ENERGY = "🟧"
    
    # EXP Bar
    EXP = "🟪"
    
    # Generic
    EMPTY = "⬜"
    FULL = "🟩"


# ============================================================================
# BAHASA INDONESIA KONSISTEN
# ============================================================================

class Lang:
    """Text dalam Bahasa Indonesia yang konsisten"""
    
    # Player Actions
    ATTACK = "Serang"
    DEFEND = "Bertahan"
    DODGE = "Menghindar"
    USE_SKILL = "Gunakan Skill"
    USE_ITEM = "Gunakan Item"
    RUN = "Kabur"
    
    # Directions
    NORTH = "Utara"
    SOUTH = "Selatan"
    EAST = "Timur"
    WEST = "Barat"
    
    # Menu
    PROFILE = "Profil"
    INVENTORY = "Tas"
    EQUIPMENT = "Peralatan"
    SKILLS = "Skill"
    QUESTS = "Misi"
    STATS = "Statistik"
    
    # Status
    HP_FULL = "HP penuh"
    MP_FULL = "MP penuh"
    ENERGY_FULL = "Energi penuh"
    
    # Combat Results
    CRITICAL = "Kritis!"
    MISS = "Meleset!"
    BLOCKED = "Ditahan!"
    DODGED = "Dihindari!"
    
    # Common Phrases
    YOU = "Kamu"
    ENEMY = "Musuh"
    DAMAGE = "Damage"
    HEAL = "Pulih"
    GAINED = "Dapat"
    LOST = "Hilang"


# ============================================================================
# QUICK TEMPLATES (Siap Pakai)
# ============================================================================

def format_stat(value, max_value=None):
    """Format angka stat dengan pemisah ribuan"""
    if max_value:
        return f"{int(value):,}/{int(max_value):,}"
    return f"{int(value):,}"


def format_currency(amount):
    """Format gold dengan pemisah ribuan"""
    return f"{Icon.GOLD} {int(amount):,}G"


def format_hp(current, maximum):
    """Format HP dengan ikon dan angka"""
    return f"{Icon.HP} {int(current)}/{int(maximum)}"


def format_mp(current, maximum):
    """Format MP dengan ikon dan angka"""
    return f"{Icon.MP} {int(current)}/{int(maximum)}"


def format_energy(current, maximum=100):
    """Format Energy dengan ikon dan angka"""
    return f"{Icon.ENERGY} {int(current)}/{int(maximum)}"


def create_separator(style="line"):
    """Buat separator sesuai style"""
    if style == "line":
        return Text.LINE
    elif style == "short":
        return Text.LINE_SHORT
    else:
        return Text.LINE
