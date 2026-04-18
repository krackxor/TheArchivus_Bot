# game/data/environment/hazards.py

"""
Hazards Database - The Archivus
Berisi daftar bahaya lingkungan yang memberikan penalti jika pemain
tidak menggunakan item pelindung (Masker, Mantel, dll).
"""

HAZARDS = {
    "RACUN": {
        "name": "Miasma Beracun",
        "desc": "Kabut hijau pekat menyelimuti area ini. Udaranya terasa berat dan berbau busuk.",
        "required_item": "item_masker_gas",
        "safe_msg": "😷 **Masker Gas** milikmu menyaring udara kotor. Kau bisa bernapas dengan lega.",
        "danger_msg": "🤢 Paru-parumu terasa terbakar! Racun miasma mulai merusak tubuhmu.",
        "penalty": {
            "hp_loss": 15,
            "status_effect": "poison",
            "effect_val": 5
        }
    },
    
    "DINGIN": {
        "name": "Suhu Sub-Zero",
        "desc": "Angin es berhembus kencang, membekukan apapun yang tidak bergerak.",
        "required_item": "item_mantel_bulu",
        "safe_msg": "🧥 **Mantel Bulu** yang tebal menjaga suhu tubuhmu tetap hangat.",
        "danger_msg": "❄️ Dingin yang ekstrem menusuk hingga ke tulang! Gerakanmu melambat.",
        "penalty": {
            "energy_loss": 20,
            "hp_loss": 5,
            "status_effect": "freeze_debuff"
        }
    },

    "GELAP": {
        "name": "Kegelapan Abyss",
        "desc": "Cahaya tidak mampu menembus area ini. Kau merasa diawasi oleh ribuan mata dari kegelapan.",
        "required_item": "item_lentera_jiwa",
        "safe_msg": "🕯️ Cahaya dari **Lentera Jiwa** mengusir bayangan jahat di sekitarmu.",
        "danger_msg": "🌑 Kegelapan mulai menggerogoti kewarasanmu. Kau merasa kehilangan arah.",
        "penalty": {
            "mp_loss": 20,
            "energy_loss": 10
        }
    },

    "RAWA": {
        "name": "Lumpur Penghisap",
        "desc": "Tanah di bawah kakimu tidak stabil dan mulai menarikmu ke bawah.",
        "required_item": "item_boots_heavy",
        "safe_msg": "🥾 **Heavy Boots** membuat pijakanmu tetap kokoh di atas lumpur.",
        "danger_msg": "⚠️ Kau terjebak dalam lumpur! Membutuhkan tenaga ekstra untuk melepaskan diri.",
        "penalty": {
            "energy_loss": 30
        }
    }
}

# --- LOGIKA INTERAKSI HAZARD ---

def process_hazard_interaction(player, hazard_type):
    """
    Memproses dampak bahaya lingkungan terhadap pemain.
    Mengembalikan: (is_safe, message)
    """
    hazard = HAZARDS.get(hazard_type)
    if not hazard:
        return True, "Area ini aman."

    required_item = hazard['required_item']
    
    # Cek apakah pemain memiliki item pelindung di inventory
    if required_item in player.get('inventory', []):
        return True, hazard['safe_msg']
    
    # Jika tidak memiliki item, terapkan penalti
    penalty = hazard['penalty']
    
    # Terapkan pengurangan HP
    if 'hp_loss' in penalty:
        player['hp'] = max(0, player.get('hp', 0) - penalty['hp_loss'])
        
    # Terapkan pengurangan Energy
    if 'energy_loss' in penalty:
        player['energy'] = max(0, player.get('energy', 100) - penalty['energy_loss'])
        
    # Terapkan pengurangan MP
    if 'mp_loss' in penalty:
        player['mp'] = max(0, player.get('mp', 0) - penalty['mp_loss'])
        
    # Terapkan efek status
    if 'status_effect' in penalty:
        if 'status_effects' not in player:
            player['status_effects'] = []
        player['status_effects'].append(penalty['status_effect'])
        
    return False, hazard['danger_msg']

def get_hazard_data(hazard_type):
    """Mengambil data bahaya berdasarkan tipe (RACUN, DINGIN, dll)."""
    return HAZARDS.get(hazard_type)

def get_all_hazards():
    """Mengambil seluruh daftar bahaya lingkungan."""
    return HAZARDS
