"""
Master Data Equipment (Weapon, Shield, Armor)
Menyimpan semua statistik dasar untuk kalkulasi combat, shop, durability, dan Soul Skills.
"""

# --- TIER MULTIPLIERS ---
# Digunakan untuk menghitung harga dan stat final
TIER_MULTIPLIERS = {
    1: {"name": "Basic", "stat_mult": 1.0, "cost_mult": 1.0},
    2: {"name": "Advanced", "stat_mult": 1.3, "cost_mult": 2.5},
    3: {"name": "Elite", "stat_mult": 1.6, "cost_mult": 5.0},
    4: {"name": "Master", "stat_mult": 2.0, "cost_mult": 10.0},
    5: {"name": "Mythic", "stat_mult": 2.5, "cost_mult": 25.0}
}

# --- WEAPONS MASTER DATA ---
WEAPONS = {
    # ONE-HANDED (Bisa pakai Shield)
    "wpn_shortsword": {
        "name": "Short Sword", "type": "1H", "base_atk": 18, "weight": 6, "speed": "fast", "base_cost": 100, "durability": 50,
        "skill": {"id": "skl_slash", "name": "Power Slash", "cost": 10, "effect": "dmg_1.5x"}
    },
    "wpn_longsword": {
        "name": "Longsword", "type": "1H", "base_atk": 24, "weight": 10, "speed": "medium", "base_cost": 150, "durability": 50,
        "skill": {"id": "skl_cleave", "name": "Cleave", "cost": 15, "effect": "dmg_1.8x"}
    },
    "wpn_katana": {
        "name": "Katana", "type": "1H", "base_atk": 27, "weight": 8, "speed": "fast", "base_cost": 250, "bonus_crit": 0.10, "durability": 50,
        "skill": {"id": "skl_iaido", "name": "Iaido Strike", "cost": 20, "effect": "dmg_2x_fast"}
    },
    "wpn_rapier": {
        "name": "Rapier", "type": "1H", "base_atk": 20, "weight": 5, "speed": "very_fast", "base_cost": 200, "durability": 50,
        "skill": {"id": "skl_pierce", "name": "Armor Pierce", "cost": 15, "effect": "ignore_def"}
    },
    "wpn_pistol": {
        "name": "Pistol", "type": "1H", "base_atk": 38, "weight": 11, "speed": "fast", "base_cost": 280, "durability": 50,
        "skill": {"id": "skl_quickdraw", "name": "Quick Draw", "cost": 15, "effect": "time_boost"}
    },
    
    # TWO-HANDED (Damage Besar, Tanpa Shield)
    "wpn_dual_sword": {
        "name": "Dual Sword", "type": "2H", "base_atk": 52, "weight": 27, "speed": "slow", "base_cost": 300, "durability": 50,
        "skill": {"id": "skl_dance", "name": "Blade Dance", "cost": 25, "effect": "multi_hit"}
    },
    "wpn_dual_dagger": {
        "name": "Dual Dagger", "type": "2H", "base_atk": 36, "weight": 14, "speed": "fast", "base_cost": 280, "bonus_crit": 0.15, "durability": 50,
        "skill": {"id": "skl_vital", "name": "Vital Strike", "cost": 20, "effect": "auto_crit"}
    },
    "wpn_great_axe": {
        "name": "Great Axe", "type": "2H", "base_atk": 44, "weight": 24, "speed": "slow", "base_cost": 220, "durability": 50,
        "skill": {"id": "skl_sunder", "name": "Sunder Armor", "cost": 25, "effect": "break_def"}
    },
    "wpn_rifle": {
        "name": "Rifle", "type": "2H", "base_atk": 62, "weight": 29, "speed": "slow", "base_cost": 400, "durability": 50,
        "skill": {"id": "skl_headshot", "name": "Snipe", "cost": 30, "effect": "huge_dmg_slow"}
    },
    "wpn_shotgun": {
        "name": "Shotgun", "type": "2H", "base_atk": 72, "weight": 34, "speed": "very_slow", "base_cost": 450, "durability": 50,
        "skill": {"id": "skl_pointblank", "name": "Point Blank", "cost": 35, "effect": "stun_target"}
    },
    "wpn_staff": {
        "name": "Magic Staff", "type": "2H", "base_atk": 28, "weight": 17, "speed": "medium", "base_cost": 200, "durability": 50, "is_magic": True
        # Skill khusus Staff ditangani oleh elemen di combat.py (get_staff_skill_info)
    },
    "wpn_unarmed": {
        "name": "Tangan Kosong", "type": "2H", "base_atk": 12, "weight": 0, "speed": "fast", "base_cost": 0, "durability": 999 
    }
}

# --- SHIELDS MASTER DATA (Opsional untuk 1H) ---
SHIELDS = {
    "shd_buckler": {
        "name": "Buckler", "base_def": 8, "weight": 3, "base_cost": 80, "bonus_dodge": 0.05, "durability": 50,
        "skill": {"id": "skl_parry", "name": "Parry Counter", "cost": 20, "effect": "reflect_100"}
    },
    "shd_round": {
        "name": "Round Shield", "base_def": 15, "weight": 8, "base_cost": 150, "durability": 50,
        "skill": {"id": "skl_bash", "name": "Shield Bash", "cost": 15, "effect": "stun_small"}
    },
    "shd_tower": {
        "name": "Tower Shield", "base_def": 25, "weight": 18, "base_cost": 300, "durability": 50,
        "skill": {"id": "skl_fortress", "name": "Iron Wall", "cost": 25, "effect": "block_all"}
    }
}

# --- ARMORS MASTER DATA ---
ARMORS = {
    "head": {
        "arm_cloth_hood": {"name": "Cloth Hood", "base_def": 8, "weight": 3, "base_cost": 50, "durability": 50},
        "arm_leather_cap": {"name": "Leather Cap", "base_def": 10, "weight": 5, "base_cost": 100, "durability": 50},
        "arm_iron_helm": {"name": "Iron Helm", "base_def": 14, "weight": 7, "base_cost": 200, "durability": 50}
    },
    "chest": {
        "arm_cloth_robe": {
            "name": "Cloth Robe", "base_def": 20, "weight": 10, "base_cost": 120, "durability": 50,
            "skill": {"id": "skl_mana_shield", "name": "Mana Shield", "cost": 20, "effect": "mp_to_hp"}
        },
        "arm_leather_armor": {
            "name": "Leather Armor", "base_def": 24, "weight": 14, "base_cost": 220, "durability": 50,
            "skill": {"id": "skl_reflex", "name": "Shadow Step", "cost": 35, "effect": "100_dodge"}
        },
        "arm_plate_armor": {
            "name": "Full Plate Armor", "base_def": 35, "weight": 25, "base_cost": 500, "durability": 50,
            "skill": {"id": "skl_reflect", "name": "Thorn Mail", "cost": 20, "effect": "reflect_dmg"}
        }
    },
    "gloves": {
        "arm_light_gloves": {"name": "Light Gloves", "base_def": 6, "weight": 2, "base_cost": 60, "bonus_type": "speed", "durability": 50},
        "arm_combat_gloves": {"name": "Combat Gauntlets", "base_def": 9, "weight": 4, "base_cost": 150, "bonus_type": "damage", "durability": 50},
        "arm_heavy_gauntlets": {"name": "Heavy Gauntlets", "base_def": 12, "weight": 6, "base_cost": 180, "bonus_type": "defense", "durability": 50}
    },
    "boots": {
        "arm_cloth_boots": {"name": "Cloth Boots", "base_def": 8, "weight": 4, "base_cost": 60, "durability": 50},
        "arm_leather_boots": {"name": "Leather Boots", "base_def": 10, "weight": 6, "base_cost": 120, "durability": 50},
        "arm_greaves": {"name": "Iron Greaves", "base_def": 14, "weight": 9, "base_cost": 220, "durability": 50}
    }
}

def get_equipment_stat(equip_id, category, tier=1):
    """
    Fungsi ajaib untuk mengambil stat final dari sebuah item berdasarkan tier-nya.
    Category bisa berupa: 'weapon', 'shield', 'head', 'chest', 'gloves', 'boots'
    """
    if category == "weapon":
        data = WEAPONS.get(equip_id)
    elif category == "shield":
        data = SHIELDS.get(equip_id)
    else:
        data = ARMORS.get(category, {}).get(equip_id)

    if not data:
        return None

    multiplier = TIER_MULTIPLIERS.get(tier, TIER_MULTIPLIERS[1])
    
    # Copy data agar tidak mengubah master data asli
    final_data = data.copy()
    final_data["tier"] = tier
    final_data["full_name"] = f"[{multiplier['name']}] {data['name']}"
    final_data["cost"] = int(data["base_cost"] * multiplier["cost_mult"])
    
    # Memastikan Max Durability terkunci di 50 (Bisa disesuaikan nanti jika butuh)
    final_data["max_durability"] = 50
    
    # Kalikan stat utama dengan tier
    if "base_atk" in final_data:
        final_data["atk"] = int(final_data["base_atk"] * multiplier["stat_mult"])
    if "base_def" in final_data:
        final_data["def"] = int(final_data["base_def"] * multiplier["stat_mult"])
        
    return final_data
