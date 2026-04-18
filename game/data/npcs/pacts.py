# game/data/npcs/pacts.py

"""
NPC Pact & Altar Database - The Archivus
Berisi entitas yang menawarkan Kontrak Darah atau Pertukaran Permanen.
Mekanik: Permanen Sacrifice vs Massive Power Up.
"""

PACT_NPCS = {
    "altar_of_excess": {
        "name": "Altar of Excess",
        "role": "pact",
        "desc": "Sebuah altar yang terbuat dari kristal merah yang berdenyut seperti jantung. Bau karat besi menyengat di sekitarnya.",
        "dialog": "Darah dibayar dengan kuasa. Kehidupan dibayar dengan kehancuran. Apakah kau siap memberikan sebagian dirimu?",
        "options": [
            {
                "title": "Kontrak Kehancuran",
                "sacrifice": {"max_hp": -20},
                "reward": {"p_atk": 15, "m_atk": 15},
                "msg": "Kau merasakan sebagian vitalitasmu terhisap, namun kekuatan murni kini mengalir di senjatamu."
            },
            {
                "title": "Kontrak Kelincahan",
                "sacrifice": {"max_hp": -10},
                "reward": {"dodge": 0.05, "speed": 10},
                "msg": "Tubuhmu terasa lebih ringan, meski detak jantungmu kini terdengar lebih lemah."
            }
        ]
    },

    "npc_veiled_specter": {
        "name": "The Veiled Specter",
        "role": "pact",
        "desc": "Sosok transparan yang memegang timbangan tua. Salah satu sisi timbangannya berisi gumpalan daging, yang lain berisi cahaya.",
        "dialog": "Keseimbangan harus dijaga, Weaver. Berikan apa yang kau miliki berlebih, dan ambillah apa yang kau butuhkan.",
        "options": [
            {
                "title": "Tukar Emas dengan Jiwa",
                "sacrifice": {"gold": -5000},
                "reward": {"max_mp": 20},
                "msg": "Emasmu menguap menjadi asap biru yang merasuki pikiranmu. Kapasitas sihirmu meningkat."
            },
            {
                "title": "Tukar Keberuntungan dengan Kekuatan",
                "sacrifice": {"crit_chance": -0.05},
                "reward": {"p_atk": 25},
                "msg": "Kau merasa dunia menjadi lebih dingin dan datar, namun otot-ototmu mengeras dengan kekuatan baru."
            }
        ]
    }
}

def get_pact_data(entity_id):
    """Mengambil data kontrak/pact berdasarkan ID."""
    return PACT_NPCS.get(entity_id)

def get_all_pacts():
    """Mengambil seluruh database pact."""
    return PACT_NPCS

def apply_pact_consequences(player, option_index, entity_id):
    """
    Logika untuk menghitung perubahan statistik setelah mengambil kontrak.
    Mengembalikan data update untuk database.
    """
    entity = get_pact_data(entity_id)
    if not entity or option_index >= len(entity['options']):
        return None
        
    option = entity['options'][option_index]
    sacrifice = option['sacrifice']
    reward = option['reward']
    
    updates = {}
    
    # Proses Pengorbanan (Sacrifice)
    for stat, val in sacrifice.items():
        updates[stat] = player.get(stat, 0) + val
        
    # Proses Hadiah (Reward)
    # Catatan: Jika reward berupa stats dasar (p_atk/p_def), 
    # sebaiknya dimasukkan ke field 'permanent_bonus' agar tidak tertimpa saat ganti gear.
    p_bonus = player.get('permanent_bonus', {})
    for stat, val in reward.items():
        p_bonus[stat] = p_bonus.get(stat, 0) + val
    
    updates['permanent_bonus'] = p_bonus
    
    return updates, option['msg']
