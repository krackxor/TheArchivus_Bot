# game/ui_constants.py

"""
UI CONSTANTS & MULTI-LANGUAGE SYSTEM - The Archivus
Pusat standarisasi ikon, pembatas (separator), dan terjemahan bahasa.
Mencakup elemen tempur, spesifikasi equipment, dan penanda lokasi.
"""

# ============================================================================
# 1. IKON SISTEM (VISUAL IDENTIFIERS)
# ============================================================================
class Icon:
    # --- Status Dasar & Atribut ---
    HP = "❤️"
    MP = "💧"
    ENERGY = "⚡"
    EXP = "✨"
    LEVEL = "🎖️"
    GOLD = "💰"
    KILLS = "💀"
    
    # --- Combat & Taktik ---
    ATTACK = "⚔️"
    DEFENSE = "🛡️"
    MAGIC = "🔮"
    SPEED = "💨"
    DODGE = "🌀"
    SKILL = "💠"
    CRITICAL = "💥"
    MISS = "💨"
    
    # --- Elemen Sihir & Status (Elements & Status Ailments) ---
    EL_FIRE = "🔥"
    EL_ICE = "❄️"
    EL_LIGHTNING = "⚡"
    EL_EARTH = "🪨"
    EL_WIND = "🌪️"
    EL_HOLY = "☀️"
    EL_DARK = "🌑"
    ST_POISON = "🦠"
    ST_BLEED = "🩸"
    ST_STUN = "😵"
    
    # --- Kategori Tas (Inventory Categories) ---
    BAG = "🎒"
    POTION = "🧪"
    FOOD = "🍖"
    MATERIAL = "🧩"
    QUEST_ITEM = "📜"
    LOOT = "🎁"
    
    # --- Equipment Spesifik (Gear Types) ---
    GEAR_SWORD = "🗡️"
    GEAR_BOW = "🏹"
    GEAR_STAFF = "🪄"
    GEAR_DAGGER = "🔪"
    GEAR_SHIELD = "🛡️"
    GEAR_HELMET = "🪖"
    GEAR_ARMOR = "🧥"
    GEAR_BOOTS = "👢"
    GEAR_RING = "💍"
    GEAR_AMULET = "📿"
    
    # --- Lokasi & Bioma (World Map & Biomes) ---
    LOC_VILLAGE = "🏘️"      # Desa
    LOC_CITY = "🏙️"         # Kota
    LOC_FOREST = "🌲"       # Hutan
    LOC_SWAMP = "🌫️"        # Rawa Beracun
    LOC_GRAVEYARD = "🪦"    # Kuburan
    LOC_DUNGEON = "⛓️"      # Dungeon / Bawah Tanah
    LOC_CASTILE = "🏰"      # Castile / Kastil End-game
    LOC_CAFE = "☕"         # Kedai / Cafe (Safezone)
    LOC_INN = "🛌"          # Penginapan
    
    # --- Entitas (Entities) ---
    NPC = "👤"
    MERCHANT = "⚖️"
    MONSTER = "🐺"
    MINIBOSS = "👹"
    BOSS = "👑"
    
    # --- Sistem & Navigasi UI ---
    ARROW_UP = "⬆️"
    ARROW_DOWN = "⬇️"
    ARROW_LEFT = "⬅️"
    ARROW_RIGHT = "➡️"
    CLOSE = "❌"
    BACK = "⬅️"
    INFO = "ℹ️"
    WARNING = "⚠️"
    SUCCESS = "✅"
    LOCK = "🔒"
    KEY = "🗝️"


# ============================================================================
# 2. TEMPLATE TEXT (PEMBATAS)
# ============================================================================
class Text:
    LINE = "━━━━━━━━━━━━━━━━━━━━"
    LINE_SHORT = "━━━━━━━━━━━━━━"


# ============================================================================
# 3. SISTEM MULTI-BAHASA (TRANSLATIONS)
# ============================================================================
TRANSLATIONS = {
    "id": { # BAHASA INDONESIA (Default)
        # Menu & UI
        "BTN_CLOSE": "❌ Tutup Menu",
        "BTN_BACK": "⬅️ Kembali",
        "INVENTORY_TITLE": "Isi Tas",
        "CONSUMABLES_TITLE": "Daftar Ramuan & Makanan",
        "PROFILE_TITLE": "Profil & Status",
        
        # Lokasi
        "AREA_VILLAGE": "Desa Berkabut",
        "AREA_CITY": "Kota Pusat",
        "AREA_FOREST": "Hutan Menyesatkan",
        "AREA_SWAMP": "Rawa Kematian",
        "AREA_GRAVEYARD": "Pemakaman Kuno",
        "AREA_DUNGEON": "Labirin Bawah Tanah",
        "AREA_CASTILE": "Castile Sang Penguasa",
        
        # Navigasi Bawah (Reply Keyboard)
        "NAV_NORTH": "⬆️ Utara",
        "NAV_SOUTH": "⬇️ Selatan",
        "NAV_WEST": "⬅️ Barat",
        "NAV_EAST": "Timur ➡️",
        "NAV_REST": "🧘 Meditasi",
        "NAV_PROFILE": "📊 Profil",
        
        # Stats & Info
        "LEVEL": "Lvl",
        "EXP": "EXP",
        "STAT_POINTS_INFO": "✨ STAT POINTS: {sp}\n_Ketuk tombol + di bawah untuk upgrade!_",
        
        # Pesan Sistem
        "EMPTY_BAG": "📭 Tas kosong.",
        "NOT_ENOUGH_GOLD": "❌ Emasmu tidak cukup!",
        "NOT_ENOUGH_ENERGY": "❌ Energimu habis! Carilah tempat beristirahat.",
        "LOCKED_DOOR": "🔒 Pintu terkunci. Membutuhkan kunci khusus.",
        
        # Taktik Pertempuran
        "CMD_ATTACK": "⚔️ Serang",
        "CMD_SKILL": "💠 Skill",
        "CMD_DEFEND": "🛡️ Bertahan",
        "CMD_DODGE": "🌀 Menghindar",
        "CMD_RUN": "🏃 Kabur"
    },
    
    "en": { # ENGLISH
        # Menu & UI
        "BTN_CLOSE": "❌ Close Menu",
        "BTN_BACK": "⬅️ Back",
        "INVENTORY_TITLE": "Inventory",
        "CONSUMABLES_TITLE": "Consumables",
        "PROFILE_TITLE": "Profile & Status",
        
        # Lokasi
        "AREA_VILLAGE": "Misty Village",
        "AREA_CITY": "Central City",
        "AREA_FOREST": "Deceiving Forest",
        "AREA_SWAMP": "Swamp of Death",
        "AREA_GRAVEYARD": "Ancient Graveyard",
        "AREA_DUNGEON": "Underground Labyrinth",
        "AREA_CASTILE": "The Sovereign's Castile",
        
        # Navigasi Bawah (Reply Keyboard)
        "NAV_NORTH": "⬆️ North",
        "NAV_SOUTH": "⬇️ South",
        "NAV_WEST": "⬅️ West",
        "NAV_EAST": "East ➡️",
        "NAV_REST": "🧘 Meditate",
        "NAV_PROFILE": "📊 Profile",
        
        # Stats & Info
        "LEVEL": "Lvl",
        "EXP": "EXP",
        "STAT_POINTS_INFO": "✨ STAT POINTS: {sp}\n_Tap the + button below to upgrade!_",
        
        # Pesan Sistem
        "EMPTY_BAG": "📭 Bag is empty.",
        "NOT_ENOUGH_GOLD": "❌ Not enough gold!",
        "NOT_ENOUGH_ENERGY": "❌ Out of energy! Find a place to rest.",
        "LOCKED_DOOR": "🔒 The door is locked. Needs a special key.",
        
        # Taktik Pertempuran
        "CMD_ATTACK": "⚔️ Attack",
        "CMD_SKILL": "💠 Skill",
        "CMD_DEFEND": "🛡️ Defend",
        "CMD_DODGE": "🌀 Dodge",
        "CMD_RUN": "🏃 Run"
    }
}

def get_text(lang_code: str, key: str, **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS["id"])
    text_template = lang_dict.get(key, f"[{key}_MISSING]")
    if kwargs:
        try:
            return text_template.format(**kwargs)
        except KeyError:
            return text_template
    return text_template
