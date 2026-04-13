"""
Master Data Equipment (Weapon, Shield, Armor)
Menyimpan semua statistik dasar untuk kalkulasi combat dan shop.
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
    "wpn_shortsword": {"name": "Short Sword", "type": "1H", "base_atk": 18, "weight": 6, "speed": "fast", "base_cost": 100},
    "wpn_longsword": {"name": "Longsword", "type": "1H", "base_atk": 24, "weight": 10, "speed": "medium", "base_cost": 150},
    "wpn_katana": {"name": "Katana", "type": "1H", "base_atk": 27, "weight": 8, "speed": "fast", "base_cost": 250, "bonus_crit": 0.10},
    "wpn_rapier": {"name": "Rapier", "type": "1H", "base_atk": 20, "weight": 5, "speed": "very_fast", "base_cost": 200},
    
    # TWO-HANDED (Damage Besar, Tanpa Shield)
    "wpn_dual_sword": {"name": "Dual Sword", "type": "2H", "base_atk": 52, "weight": 27, "speed": "slow", "base_cost": 300},
    "wpn_dual_dagger": {"name": "Dual Dagger", "type": "2H", "base_atk": 36, "weight": 14, "speed": "fast", "base_cost": 280, "bonus_crit": 0.15},
    "wpn_great_axe": {"name": "Great Axe", "type": "2H", "base_atk": 44, "weight": 24, "speed": "slow", "base_cost": 220},
    "wpn_staff": {"name": "Magic Staff", "type": "2H", "base_atk": 28, "weight": 17, "speed": "medium", "base_cost": 200, "is_magic": True},
    "wpn_unarmed": {"name": "Tangan Kosong", "type": "2H", "base_atk": 12, "weight": 0, "speed": "fast", "base_cost": 0}
}

# --- SHIELDS MASTER DATA (Opsional untuk 1H) ---
SHIELDS = {
    "shd_buckler": {"name": "Buckler", "base_def": 8, "weight": 3, "base_cost": 80, "bonus_dodge": 0.05},
    "shd_round": {"name": "Round Shield", "base_def": 15, "weight": 8, "base_cost": 150},
    "shd_tower": {"name": "Tower Shield", "base_def": 25, "weight": 18, "base_cost": 300}
}

# --- ARMORS MASTER DATA ---
ARMORS = {
    "head": {
        "arm_cloth_hood": {"name": "Cloth Hood", "base_def": 8, "weight": 3, "base_cost": 50},
        "arm_leather_cap": {"name": "Leather Cap", "base_def": 10, "weight": 5, "base_cost": 100},
        "arm_iron_helm": {"name": "Iron Helm", "base_def": 14, "weight": 7, "base_cost": 200}
    },
    "chest": {
        "arm_cloth_robe": {"name": "Cloth Robe", "base_def": 20, "weight": 10, "base_cost": 120},
        "arm_leather_armor": {"name": "Leather Armor", "base_def": 24, "weight": 14, "base_cost": 220},
        "arm_plate_armor": {"name": "Full Plate Armor", "base_def": 35, "weight": 25, "base_cost": 500}
    },
    "gloves": {
        "arm_light_gloves": {"name": "Light Gloves", "base_def": 6, "weight": 2, "base_cost": 60, "bonus_type": "speed"},
        "arm_combat_gloves": {"name": "Combat Gauntlets", "base_def": 9, "weight": 4, "base_cost": 150, "bonus_type": "damage"},
        "arm_heavy_gauntlets": {"name": "Heavy Gauntlets", "base_def": 12, "weight": 6, "base_cost": 180, "bonus_type": "defense"}
    },
    "boots": {
        "arm_cloth_boots": {"name": "Cloth Boots", "base_def": 8, "weight": 4, "base_cost": 60},
        "arm_leather_boots": {"name": "Leather Boots", "base_def": 10, "weight": 6, "base_cost": 120},
        "arm_greaves": {"name": "Iron Greaves", "base_def": 14, "weight": 9, "base_cost": 220}
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
    
    # Kalikan stat utama dengan tier
    if "base_atk" in final_data:
        final_data["atk"] = int(final_data["base_atk"] * multiplier["stat_mult"])
    if "base_def" in final_data:
        final_data["def"] = int(final_data["base_def"] * multiplier["stat_mult"])
        
    return final_data
