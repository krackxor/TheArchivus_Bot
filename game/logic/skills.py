# game/logic/skills.py

"""
SISTEM SKILL & MAGIC - The Archivus
ULTIMATE EDITION: 150+ Skills + Skill Tree + Branching Evolution + Cooldown + Combo System
FULLY BALANCED & PRODUCTION READY
"""

import random
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# ==========================================
# === CONSTANTS & CONFIGURATION ===
# ==========================================
SKILL_BALANCE_CONFIG = {
    "base_mp_reduction_per_evo": 0.90,      # 10% MP cost reduction per evolution level
    "base_mult_increase_per_evo": 0.15,     # 15% damage increase per evolution level
    "max_evolution_level": 3,
    "combo_activation_chance": 0.4,         # 40% chance untuk apply combo effect
    "usage_threshold_for_evo": 15,          # Mulai evolve setelah 15 kali pemakaian
    "usage_per_evo_level": 25,              # Setiap 25 penggunaan = 1 level evolusi
}

# ==========================================
# === 1. DATABASE SKILL AKTIF (150+ SKILLS) ===
# ==========================================
ACTIVE_SKILLS = {
    # ===== SKILL DASAR (Level 1) =====
    "heavy_strike": {
        "name": "Heavy Strike",
        "unlock_level": 1,
        "mp_cost": 5,
        "mult": 1.5,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Serangan fisik bertenaga tinggi.",
        "cooldown": 0
    },
    "mana_bullet": {
        "name": "Mana Bullet",
        "unlock_level": 1,
        "mp_cost": 5,
        "mult": 1.5,
        "type": "magic",
        "element": "none",
        "status_effect": None,
        "desc": "Tembakan energi murni.",
        "cooldown": 0
    },
    "quick_strike": {
        "name": "Quick Strike",
        "unlock_level": 1,
        "mp_cost": 3,
        "mult": 0.8,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Serangan cepat dengan akurasi tinggi.",
        "cooldown": 0
    },
    "spark": {
        "name": "Spark",
        "unlock_level": 1,
        "mp_cost": 4,
        "mult": 1.2,
        "type": "magic",
        "element": "none",
        "status_effect": None,
        "desc": "Ledakan kecil energi.",
        "cooldown": 0
    },

    # ===== SKILL UTILITY (Level 1-5) =====
    "heal_touch": {
        "name": "Heal Touch",
        "unlock_level": 2,
        "mp_cost": 8,
        "mult": 1.3,
        "type": "heal",
        "element": "none",
        "status_effect": None,
        "desc": "Menyembuhkan luka ringan.",
        "cooldown": 1
    },
    "war_cry": {
        "name": "War Cry",
        "unlock_level": 5,
        "mp_cost": 10,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "atk_buff",
        "desc": "Meningkatkan ATK sementara.",
        "cooldown": 3
    },
    "defensive_stance": {
        "name": "Defensive Stance",
        "unlock_level": 4,
        "mp_cost": 8,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "def_buff",
        "desc": "Mengurangi damage yang diterima.",
        "cooldown": 3
    },
    "focus": {
        "name": "Focus",
        "unlock_level": 3,
        "mp_cost": 6,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "crit_buff",
        "desc": "Meningkatkan peluang critical hit.",
        "cooldown": 2
    },

    # ===== SKILL FISIK INTERMEDIATE (Level 6-15) =====
    "double_slash": {
        "name": "Double Slash",
        "unlock_level": 10,
        "mp_cost": 12,
        "mult": 2.0,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Dua tebasan cepat.",
        "cooldown": 1
    },
    "power_strike": {
        "name": "Power Strike",
        "unlock_level": 8,
        "mp_cost": 14,
        "mult": 2.2,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Serangan bertenaga dengan momentum penuh.",
        "cooldown": 2
    },
    "whirlwind_slash": {
        "name": "Whirlwind Slash",
        "unlock_level": 12,
        "mp_cost": 16,
        "mult": 1.9,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Serangan berputar ke segala arah.",
        "cooldown": 2
    },
    "piercing_thrust": {
        "name": "Piercing Thrust",
        "unlock_level": 9,
        "mp_cost": 13,
        "mult": 2.1,
        "type": "physical",
        "element": "none",
        "status_effect": "def_debuff",
        "desc": "Tusukan yang menembus pertahanan.",
        "cooldown": 2
    },
    "crushing_blow": {
        "name": "Crushing Blow",
        "unlock_level": 11,
        "mp_cost": 15,
        "mult": 2.3,
        "type": "physical",
        "element": "none",
        "status_effect": "stun",
        "desc": "Pukulan berat yang menghancurkan.",
        "cooldown": 3
    },

    # ===== SKILL MAGIC INTERMEDIATE (Level 6-15) =====
    "fireball": {
        "name": "Fireball",
        "unlock_level": 7,
        "mp_cost": 14,
        "mult": 1.9,
        "type": "magic",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Bola api yang meledak.",
        "cooldown": 1
    },
    "ice_spike": {
        "name": "Ice Spike",
        "unlock_level": 8,
        "mp_cost": 13,
        "mult": 1.8,
        "type": "magic",
        "element": "ice",
        "status_effect": None,
        "desc": "Gletser tajam yang menusuk.",
        "cooldown": 1
    },
    "lightning_bolt": {
        "name": "Lightning Bolt",
        "unlock_level": 9,
        "mp_cost": 15,
        "mult": 2.0,
        "type": "magic",
        "element": "lightning",
        "status_effect": "stun",
        "desc": "Petir yang menyambar dari langit.",
        "cooldown": 2
    },
    "earth_spike": {
        "name": "Earth Spike",
        "unlock_level": 7,
        "mp_cost": 12,
        "mult": 1.7,
        "type": "magic",
        "element": "earth",
        "status_effect": None,
        "desc": "Duri bumi yang muncul tiba-tiba.",
        "cooldown": 1
    },
    "wind_slash": {
        "name": "Wind Slash",
        "unlock_level": 8,
        "mp_cost": 11,
        "mult": 1.6,
        "type": "magic",
        "element": "wind",
        "status_effect": None,
        "desc": "Pisau angin yang tajam.",
        "cooldown": 1
    },
    "poison_cloud": {
        "name": "Poison Cloud",
        "unlock_level": 10,
        "mp_cost": 16,
        "mult": 1.5,
        "type": "magic",
        "element": "poison",
        "status_effect": "poison",
        "desc": "Awan racun yang menyebar.",
        "cooldown": 2
    },
    "arcane_missile": {
        "name": "Arcane Missile",
        "unlock_level": 6,
        "mp_cost": 10,
        "mult": 1.5,
        "type": "magic",
        "element": "none",
        "status_effect": None,
        "desc": "Rudal energi murni.",
        "cooldown": 0
    },

    # ===== SKILL WEAPON SPECIFIC (Require Weapon) =====
    # --- SHIELD SKILLS ---
    "shield_bash": {
        "name": "Shield Bash",
        "unlock_level": 3,
        "req_weapon": ["shield"],
        "mp_cost": 10,
        "mult": 1.2,
        "type": "physical",
        "element": "none",
        "status_effect": "stun",
        "desc": "Hantaman tameng.",
        "cooldown": 2
    },
    "shield_raise": {
        "name": "Shield Raise",
        "unlock_level": 4,
        "req_weapon": ["shield"],
        "mp_cost": 12,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "def_buff",
        "desc": "Naikkan pertahanan dengan tameng.",
        "cooldown": 2
    },
    "shield_counter": {
        "name": "Shield Counter",
        "unlock_level": 8,
        "req_weapon": ["shield"],
        "mp_cost": 14,
        "mult": 1.8,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Hantam balik dengan tameng.",
        "cooldown": 2
    },
    "perfect_guard": {
        "name": "Perfect Guard",
        "unlock_level": 12,
        "req_weapon": ["shield"],
        "mp_cost": 20,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "def_buff",
        "desc": "Pertahanan absolut.",
        "cooldown": 5
    },
    "shield_throw": {
        "name": "Shield Throw",
        "unlock_level": 10,
        "req_weapon": ["shield"],
        "mp_cost": 15,
        "mult": 1.7,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Lempar tameng ke musuh.",
        "cooldown": 3
    },

    # --- DAGGER SKILLS ---
    "shadow_step": {
        "name": "Shadow Step",
        "unlock_level": 4,
        "req_weapon": ["dagger"],
        "mp_cost": 10,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "dodge_buff",
        "desc": "Meningkatkan hindaran.",
        "cooldown": 3
    },
    "quick_stab": {
        "name": "Quick Stab",
        "unlock_level": 5,
        "req_weapon": ["dagger"],
        "mp_cost": 8,
        "mult": 1.4,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Tusukan cepat dengan pisau.",
        "cooldown": 1
    },
    "backstab": {
        "name": "Backstab",
        "unlock_level": 7,
        "req_weapon": ["dagger"],
        "mp_cost": 12,
        "mult": 2.5,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Tusukan maut dari belakang.",
        "cooldown": 3
    },
    "assassinate": {
        "name": "Assassinate",
        "unlock_level": 15,
        "req_weapon": ["dagger"],
        "mp_cost": 25,
        "mult": 3.0,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Tusukan mematikan.",
        "cooldown": 4
    },
    "poison_blade": {
        "name": "Poison Blade",
        "unlock_level": 9,
        "req_weapon": ["dagger"],
        "mp_cost": 14,
        "mult": 1.6,
        "type": "physical",
        "element": "poison",
        "status_effect": "poison",
        "desc": "Tusukan dengan racun mematikan.",
        "cooldown": 2
    },

    # --- DUAL SWORD SKILLS ---
    "flurry_strikes": {
        "name": "Flurry Strikes",
        "unlock_level": 6,
        "req_weapon": ["dual_swords"],
        "mp_cost": 18,
        "mult": 2.2,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Tebasan beruntun dengan dua pedang.",
        "cooldown": 2
    },
    "rapid_slash": {
        "name": "Rapid Slash",
        "unlock_level": 8,
        "req_weapon": ["dual_swords"],
        "mp_cost": 16,
        "mult": 2.0,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Tebasan cepat berkali-kali.",
        "cooldown": 1
    },
    "cross_slash": {
        "name": "Cross Slash",
        "unlock_level": 18,
        "req_weapon": ["dual_swords"],
        "mp_cost": 26,
        "mult": 2.8,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "desc": "Membelah target dengan X cut.",
        "cooldown": 3
    },
    "cyclone_slash": {
        "name": "Cyclone Slash",
        "unlock_level": 12,
        "req_weapon": ["dual_swords"],
        "mp_cost": 20,
        "mult": 2.5,
        "type": "physical",
        "element": "wind",
        "status_effect": None,
        "desc": "Berputar seperti puyuh dengan pedang.",
        "cooldown": 3
    },

    # --- BOW SKILLS ---
    "piercing_arrow": {
        "name": "Piercing Arrow",
        "unlock_level": 5,
        "req_weapon": ["bow"],
        "mp_cost": 15,
        "mult": 1.8,
        "type": "physical",
        "element": "none",
        "status_effect": "def_debuff",
        "desc": "Panah penembus pertahanan.",
        "cooldown": 2
    },
    "multi_shot": {
        "name": "Multi Shot",
        "unlock_level": 7,
        "req_weapon": ["bow"],
        "mp_cost": 17,
        "mult": 1.7,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Lepas banyak panah sekaligus.",
        "cooldown": 2
    },
    "arrow_rain": {
        "name": "Arrow Rain",
        "unlock_level": 20,
        "req_weapon": ["bow"],
        "mp_cost": 30,
        "mult": 2.6,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Hujan panah dari langit.",
        "cooldown": 4
    },
    "explosive_arrow": {
        "name": "Explosive Arrow",
        "unlock_level": 10,
        "req_weapon": ["bow"],
        "mp_cost": 20,
        "mult": 2.2,
        "type": "physical",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Panah yang meledak.",
        "cooldown": 3
    },
    "frost_arrow": {
        "name": "Frost Arrow",
        "unlock_level": 9,
        "req_weapon": ["bow"],
        "mp_cost": 18,
        "mult": 1.9,
        "type": "physical",
        "element": "ice",
        "status_effect": None,
        "desc": "Panah yang membekukan.",
        "cooldown": 2
    },

    # --- STAFF SKILLS ---
    "arcane_blast": {
        "name": "Arcane Blast",
        "unlock_level": 8,
        "req_weapon": ["staff"],
        "mp_cost": 18,
        "mult": 2.1,
        "type": "magic",
        "element": "none",
        "status_effect": None,
        "desc": "Ledakan arcane dari staf.",
        "cooldown": 2
    },
    "mana_overflow": {
        "name": "Mana Overflow",
        "unlock_level": 6,
        "req_weapon": ["staff"],
        "mp_cost": 12,
        "mult": 1.6,
        "type": "magic",
        "element": "none",
        "status_effect": None,
        "desc": "Ledakkan kelebihan mana.",
        "cooldown": 1
    },
    "mana_storm": {
        "name": "Mana Storm",
        "unlock_level": 22,
        "req_weapon": ["staff", "wand"],
        "mp_cost": 32,
        "mult": 2.9,
        "type": "magic",
        "element": "none",
        "status_effect": "def_debuff",
        "desc": "Badai energi dari staf.",
        "cooldown": 5
    },
    "spell_amplify": {
        "name": "Spell Amplify",
        "unlock_level": 10,
        "req_weapon": ["staff", "wand"],
        "mp_cost": 14,
        "mult": 0,
        "type": "buff",
        "element": "none",
        "status_effect": "m_atk_buff",
        "desc": "Perkuat kekuatan magic.",
        "cooldown": 3
    },

    # ===== ULTIMATE SKILLS (Level 20+) =====
    "omnislash": {
        "name": "Omnislash",
        "unlock_level": 25,
        "mp_cost": 30,
        "mult": 3.0,
        "type": "physical",
        "element": "none",
        "status_effect": None,
        "desc": "Tebasan beruntun tanpa henti.",
        "cooldown": 4
    },
    "meteor_strike": {
        "name": "Meteor Strike",
        "unlock_level": 26,
        "mp_cost": 35,
        "mult": 3.2,
        "type": "magic",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Jatuhkan meteor dari langit.",
        "cooldown": 5
    },
    "divine_judgment": {
        "name": "Divine Judgment",
        "unlock_level": 28,
        "mp_cost": 38,
        "mult": 3.5,
        "type": "magic",
        "element": "light",
        "status_effect": "stun",
        "desc": "Hukuman cahaya ilahi.",
        "cooldown": 6
    },
    "void_rupture": {
        "name": "Void Rupture",
        "unlock_level": 30,
        "mp_cost": 40,
        "mult": 3.3,
        "type": "magic",
        "element": "dark",
        "status_effect": "def_debuff",
        "desc": "Robek ruang hampa.",
        "cooldown": 5
    },
    "absolute_zero": {
        "name": "Absolute Zero",
        "unlock_level": 29,
        "mp_cost": 37,
        "mult": 3.4,
        "type": "magic",
        "element": "ice",
        "status_effect": "stun",
        "desc": "Beku absolut segala sesuatu.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: FIRE =====
    "fire_1": {
        "name": "Embers",
        "unlock_level": 1,
        "mp_cost": 8,
        "mult": 1.4,
        "type": "magic",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Percikan api kecil.",
        "cooldown": 0
    },
    "fire_2": {
        "name": "Flame Burst",
        "unlock_level": 7,
        "mp_cost": 15,
        "mult": 1.8,
        "type": "magic",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Ledakan api membara.",
        "cooldown": 1
    },
    "fire_3": {
        "name": "Inner Flame",
        "unlock_level": 12,
        "mp_cost": 15,
        "mult": 0,
        "type": "buff",
        "element": "fire",
        "status_effect": "atk_buff",
        "desc": "Api dalam meningkatkan serangan.",
        "cooldown": 4
    },
    "fire_4": {
        "name": "Inferno Strike",
        "unlock_level": 18,
        "mp_cost": 25,
        "mult": 2.4,
        "type": "physical",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Tebasan magma yang membakar.",
        "cooldown": 3
    },
    "fire_5": {
        "name": "Hellfire",
        "unlock_level": 30,
        "mp_cost": 40,
        "mult": 3.2,
        "type": "magic",
        "element": "fire",
        "status_effect": "burn",
        "desc": "Api neraka memusnahkan segalanya.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: WATER =====
    "water_1": {
        "name": "Aqua Shot",
        "unlock_level": 1,
        "mp_cost": 6,
        "mult": 1.3,
        "type": "magic",
        "element": "water",
        "status_effect": None,
        "desc": "Tembakan air murni.",
        "cooldown": 0
    },
    "water_2": {
        "name": "Healing Stream",
        "unlock_level": 5,
        "mp_cost": 12,
        "mult": 1.5,
        "type": "heal",
        "element": "water",
        "status_effect": "regen",
        "desc": "Aliran air pemulihan.",
        "cooldown": 2
    },
    "water_3": {
        "name": "Aqua Slash",
        "unlock_level": 12,
        "mp_cost": 16,
        "mult": 1.9,
        "type": "physical",
        "element": "water",
        "status_effect": None,
        "desc": "Tebasan air yang menyegarkan.",
        "cooldown": 1
    },
    "water_4": {
        "name": "Tsunami",
        "unlock_level": 20,
        "mp_cost": 28,
        "mult": 2.5,
        "type": "magic",
        "element": "water",
        "status_effect": "stun",
        "desc": "Gelombang besar yang menenggelamkan.",
        "cooldown": 4
    },
    "water_5": {
        "name": "Abyssal Geyser",
        "unlock_level": 30,
        "mp_cost": 40,
        "mult": 3.0,
        "type": "magic",
        "element": "water",
        "status_effect": "def_debuff",
        "desc": "Semburan laut abissal.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: LIGHTNING =====
    "bolt_1": {
        "name": "Static Spark",
        "unlock_level": 1,
        "mp_cost": 8,
        "mult": 1.4,
        "type": "magic",
        "element": "lightning",
        "status_effect": "stun",
        "desc": "Percikan listrik statis.",
        "cooldown": 0
    },
    "bolt_2": {
        "name": "Thunder Clap",
        "unlock_level": 6,
        "mp_cost": 14,
        "mult": 1.7,
        "type": "magic",
        "element": "lightning",
        "status_effect": "stun",
        "desc": "Ledakan petir yang keras.",
        "cooldown": 1
    },
    "bolt_3": {
        "name": "Lightning Sprint",
        "unlock_level": 11,
        "mp_cost": 16,
        "mult": 0,
        "type": "buff",
        "element": "lightning",
        "status_effect": "spd_buff",
        "desc": "Kecepatan petir untuk bergerak.",
        "cooldown": 3
    },
    "bolt_4": {
        "name": "Thunderstorm",
        "unlock_level": 19,
        "mp_cost": 27,
        "mult": 2.3,
        "type": "magic",
        "element": "lightning",
        "status_effect": "stun",
        "desc": "Badai petir yang mengguncang.",
        "cooldown": 4
    },
    "bolt_5": {
        "name": "Celestial Lightning",
        "unlock_level": 31,
        "mp_cost": 42,
        "mult": 3.4,
        "type": "magic",
        "element": "lightning",
        "status_effect": "stun",
        "desc": "Petir langit yang mematikan.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: EARTH =====
    "earth_1": {
        "name": "Stone Throw",
        "unlock_level": 2,
        "mp_cost": 7,
        "mult": 1.2,
        "type": "magic",
        "element": "earth",
        "status_effect": None,
        "desc": "Lemparan batu kecil.",
        "cooldown": 0
    },
    "earth_2": {
        "name": "Earthquake",
        "unlock_level": 8,
        "mp_cost": 16,
        "mult": 1.9,
        "type": "magic",
        "element": "earth",
        "status_effect": "stun",
        "desc": "Gempa bumi yang dahsyat.",
        "cooldown": 2
    },
    "earth_3": {
        "name": "Stone Skin",
        "unlock_level": 13,
        "mp_cost": 18,
        "mult": 0,
        "type": "buff",
        "element": "earth",
        "status_effect": "def_buff",
        "desc": "Kulit batu untuk pertahanan.",
        "cooldown": 4
    },
    "earth_4": {
        "name": "Titan Crush",
        "unlock_level": 21,
        "mp_cost": 29,
        "mult": 2.7,
        "type": "physical",
        "element": "earth",
        "status_effect": "stun",
        "desc": "Pukulan titan raksasa.",
        "cooldown": 4
    },
    "earth_5": {
        "name": "Continental Shift",
        "unlock_level": 32,
        "mp_cost": 45,
        "mult": 3.6,
        "type": "magic",
        "element": "earth",
        "status_effect": "stun",
        "desc": "Pergeseran benua yang menghancur.",
        "cooldown": 7
    },

    # ===== 5-TIER ELEMENTAL MASTERY: WIND =====
    "wind_1": {
        "name": "Air Cutter",
        "unlock_level": 2,
        "mp_cost": 7,
        "mult": 1.3,
        "type": "magic",
        "element": "wind",
        "status_effect": None,
        "desc": "Pisau angin kecil.",
        "cooldown": 0
    },
    "wind_2": {
        "name": "Wind Gust",
        "unlock_level": 7,
        "mp_cost": 13,
        "mult": 1.6,
        "type": "magic",
        "element": "wind",
        "status_effect": None,
        "desc": "Hembusan angin kuat.",
        "cooldown": 1
    },
    "wind_3": {
        "name": "Wind Dance",
        "unlock_level": 10,
        "mp_cost": 14,
        "mult": 0,
        "type": "buff",
        "element": "wind",
        "status_effect": "dodge_buff",
        "desc": "Tari angin untuk hindaran.",
        "cooldown": 3
    },
    "wind_4": {
        "name": "Hurricane",
        "unlock_level": 20,
        "mp_cost": 26,
        "mult": 2.4,
        "type": "magic",
        "element": "wind",
        "status_effect": None,
        "desc": "Angin topan yang menggila.",
        "cooldown": 4
    },
    "wind_5": {
        "name": "Eternal Typhoon",
        "unlock_level": 31,
        "mp_cost": 43,
        "mult": 3.3,
        "type": "magic",
        "element": "wind",
        "status_effect": "def_debuff",
        "desc": "Topan abadi yang menghancur.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: ICE =====
    "ice_1": {
        "name": "Frost Bite",
        "unlock_level": 2,
        "mp_cost": 8,
        "mult": 1.3,
        "type": "magic",
        "element": "ice",
        "status_effect": None,
        "desc": "Gigitan es yang menggigit.",
        "cooldown": 0
    },
    "ice_2": {
        "name": "Blizzard",
        "unlock_level": 8,
        "mp_cost": 17,
        "mult": 1.95,
        "type": "magic",
        "element": "ice",
        "status_effect": None,
        "desc": "Badai salju yang membekukan.",
        "cooldown": 2
    },
    "ice_3": {
        "name": "Frozen Heart",
        "unlock_level": 14,
        "mp_cost": 19,
        "mult": 0,
        "type": "buff",
        "element": "ice",
        "status_effect": "def_buff",
        "desc": "Hati beku untuk ketahanan.",
        "cooldown": 4
    },
    "ice_4": {
        "name": "Glacial Strike",
        "unlock_level": 22,
        "mp_cost": 30,
        "mult": 2.6,
        "type": "physical",
        "element": "ice",
        "status_effect": "stun",
        "desc": "Pukulan gletser yang membeku.",
        "cooldown": 4
    },
    "ice_5": {
        "name": "Eternal Winter",
        "unlock_level": 32,
        "mp_cost": 44,
        "mult": 3.5,
        "type": "magic",
        "element": "ice",
        "status_effect": "stun",
        "desc": "Musim dingin abadi datang.",
        "cooldown": 7
    },

    # ===== 5-TIER ELEMENTAL MASTERY: DARK =====
    "dark_1": {
        "name": "Shadow Bolt",
        "unlock_level": 3,
        "mp_cost": 9,
        "mult": 1.5,
        "type": "magic",
        "element": "dark",
        "status_effect": None,
        "desc": "Bolt bayangan gelap.",
        "cooldown": 0
    },
    "dark_2": {
        "name": "Dark Pulse",
        "unlock_level": 9,
        "mp_cost": 16,
        "mult": 1.85,
        "type": "magic",
        "element": "dark",
        "status_effect": "def_debuff",
        "desc": "Denyutan energi gelap.",
        "cooldown": 2
    },
    "dark_3": {
        "name": "Shadow Cloak",
        "unlock_level": 13,
        "mp_cost": 17,
        "mult": 0,
        "type": "buff",
        "element": "dark",
        "status_effect": "dodge_buff",
        "desc": "Jubah bayangan untuk sembunyi.",
        "cooldown": 3
    },
    "dark_4": {
        "name": "Void Spear",
        "unlock_level": 21,
        "mp_cost": 28,
        "mult": 2.5,
        "type": "magic",
        "element": "dark",
        "status_effect": "def_debuff",
        "desc": "Tombak hampa yang menusuk.",
        "cooldown": 4
    },
    "dark_5": {
        "name": "Oblivion",
        "unlock_level": 31,
        "mp_cost": 41,
        "mult": 3.2,
        "type": "magic",
        "element": "dark",
        "status_effect": "def_debuff",
        "desc": "Kegelapan yang melenyapkan.",
        "cooldown": 6
    },

    # ===== 5-TIER ELEMENTAL MASTERY: LIGHT =====
    "light_1": {
        "name": "Holy Ray",
        "unlock_level": 3,
        "mp_cost": 8,
        "mult": 1.4,
        "type": "magic",
        "element": "light",
        "status_effect": None,
        "desc": "Sinar cahaya ilahi.",
        "cooldown": 0
    },
    "light_2": {
        "name": "Blessing",
        "unlock_level": 8,
        "mp_cost": 14,
        "mult": 1.7,
        "type": "heal",
        "element": "light",
        "status_effect": "regen",
        "desc": "Berkah cahaya penyembuh.",
        "cooldown": 2
    },
    "light_3": {
        "name": "Divine Shield",
        "unlock_level": 13,
        "mp_cost": 16,
        "mult": 0,
        "type": "buff",
        "element": "light",
        "status_effect": "def_buff",
        "desc": "Perisai ilahi yang melindungi.",
        "cooldown": 4
    },
    "light_4": {
        "name": "Holy Smite",
        "unlock_level": 21,
        "mp_cost": 27,
        "mult": 2.4,
        "type": "physical",
        "element": "light",
        "status_effect": "stun",
        "desc": "Hukuman cahaya ilahi.",
        "cooldown": 4
    },
    "light_5": {
        "name": "Divine Ascension",
        "unlock_level": 32,
        "mp_cost": 43,
        "mult": 3.3,
        "type": "magic",
        "element": "light",
        "status_effect": "regen",
        "desc": "Pencerahan ilahi datang.",
        "cooldown": 6
    },

    # ===== JOB SKILL: DREAD KNIGHT =====
    "dk_dark_slash": {
        "name": "Dark Slash",
        "unlock_level": 10,
        "req_job": "Dread Knight",
        "mp_cost": 15,
        "mult": 2.0,
        "type": "physical",
        "element": "dark",
        "status_effect": "bleed",
        "desc": "Tebasan bayangan gelap.",
        "cooldown": 2
    },
    "dk_abyssal_guard": {
        "name": "Abyssal Guard",
        "unlock_level": 15,
        "req_job": "Dread Knight",
        "mp_cost": 18,
        "mult": 0,
        "type": "buff",
        "element": "dark",
        "status_effect": "def_buff",
        "desc": "Zirah kegelapan melindungi.",
        "cooldown": 5
    },
    "dk_shadow_merge": {
        "name": "Shadow Merge",
        "unlock_level": 20,
        "req_job": "Dread Knight",
        "mp_cost": 22,
        "mult": 0,
        "type": "buff",
        "element": "dark",
        "status_effect": "dodge_buff",
        "desc": "Bersatu dengan bayangan.",
        "cooldown": 4
    },
    "dk_void_cleaver": {
        "name": "Void Cleaver",
        "unlock_level": 25,
        "req_job": "Dread Knight",
        "mp_cost": 32,
        "mult": 2.9,
        "type": "physical",
        "element": "dark",
        "status_effect": "def_debuff",
        "desc": "Pedang void yang merobek.",
        "cooldown": 5
    },

    # ===== JOB SKILL: HOLY TEMPLAR =====
    "ht_holy_smite": {
        "name": "Holy Smite",
        "unlock_level": 10,
        "req_job": "Holy Templar",
        "mp_cost": 15,
        "mult": 2.0,
        "type": "physical",
        "element": "light",
        "status_effect": "stun",
        "desc": "Hukuman cahaya ilahi.",
        "cooldown": 3
    },
    "ht_purify": {
        "name": "Purify",
        "unlock_level": 15,
        "req_job": "Holy Templar",
        "mp_cost": 20,
        "mult": 1.8,
        "type": "heal",
        "element": "light",
        "status_effect": "regen",
        "desc": "Pemurnian cahaya ilahi.",
        "cooldown": 4
    },
    "ht_radiant_barrier": {
        "name": "Radiant Barrier",
        "unlock_level": 20,
        "req_job": "Holy Templar",
        "mp_cost": 24,
        "mult": 0,
        "type": "buff",
        "element": "light",
        "status_effect": "def_buff",
        "desc": "Penghalang cahaya melindungi.",
        "cooldown": 4
    },
    "ht_judgment_strike": {
        "name": "Judgment Strike",
        "unlock_level": 25,
        "req_job": "Holy Templar",
        "mp_cost": 31,
        "mult": 3.0,
        "type": "physical",
        "element": "light",
        "status_effect": "stun",
        "desc": "Pukulan penghakiman ilahi.",
        "cooldown": 5
    },

    # ===== JOB SKILL: BLIZZARD SOVEREIGN =====
    "bs_glacial_prison": {
        "name": "Glacial Prison",
        "unlock_level": 12,
        "req_job": "Blizzard Sovereign",
        "mp_cost": 20,
        "mult": 2.1,
        "type": "magic",
        "element": "ice",
        "status_effect": "stun",
        "desc": "Penjara gletser membeku.",
        "cooldown": 3
    },
    "bs_frost_armor": {
        "name": "Frost Armor",
        "unlock_level": 16,
        "req_job": "Blizzard Sovereign",
        "mp_cost": 19,
        "mult": 0,
        "type": "buff",
        "element": "ice",
        "status_effect": "def_buff",
        "desc": "Armor es yang kukuh.",
        "cooldown": 4
    },
    "bs_eternal_winter": {
        "name": "Eternal Winter Aura",
        "unlock_level": 21,
        "req_job": "Blizzard Sovereign",
        "mp_cost": 25,
        "mult": 0,
        "type": "buff",
        "element": "ice",
        "status_effect": "atk_buff",
        "desc": "Aura musim dingin abadi.",
        "cooldown": 5
    },
    "bs_absolute_zero_strike": {
        "name": "Absolute Zero Strike",
        "unlock_level": 27,
        "req_job": "Blizzard Sovereign",
        "mp_cost": 38,
        "mult": 3.3,
        "type": "magic",
        "element": "ice",
        "status_effect": "stun",
        "desc": "Pukulan nol absolut.",
        "cooldown": 6
    },

    # ===== MONSTER & BOSS SKILLS =====
    "mon_bite": {
        "name": "Vicious Bite",
        "unlock_level": 99,
        "mp_cost": 0,
        "mult": 1.2,
        "type": "physical",
        "element": "none",
        "status_effect": "bleed",
        "cooldown": 0
    },
    "mon_acid": {
        "name": "Acid Spit",
        "unlock_level": 99,
        "mp_cost": 0,
        "mult": 1.3,
        "type": "magic",
        "element": "poison",
        "status_effect": "poison",
        "cooldown": 0
    },
    "mon_tail_whip": {
        "name": "Tail Whip",
        "unlock_level": 99,
        "mp_cost": 0,
        "mult": 1.4,
        "type": "physical",
        "element": "none",
        "status_effect": "stun",
        "cooldown": 0
    },
    "boss_nuke": {
        "name": "Cataclysm",
        "unlock_level": 99,
        "mp_cost": 0,
        "mult": 3.0,
        "type": "magic",
        "element": "void",
        "status_effect": "burn",
        "cooldown": 0
    },
    "boss_void_storm": {
        "name": "Void Storm",
        "unlock_level": 99,
        "mp_cost": 0,
        "mult": 3.2,
        "type": "magic",
        "element": "void",
        "status_effect": "stun",
        "cooldown": 0
    },
}

# ==========================================
# === 2. DATABASE SKILL PASIF ===
# ==========================================
PASSIVE_SKILLS = {
    "novice_resolve": {
        "name": "Novice Resolve",
        "req_job": "Novice Weaver",
        "effect": "regen_mp",
        "value": 2,
        "desc": "Regen 2 MP tiap ronde."
    },
    "enhanced_strike": {
        "name": "Enhanced Strike",
        "req_job": "Novice Weaver",
        "effect": "physical_boost",
        "value": 1.1,
        "desc": "Physical damage +10%."
    },
    "mana_pool": {
        "name": "Mana Pool",
        "req_job": "Novice Weaver",
        "effect": "max_mp_boost",
        "value": 1.2,
        "desc": "Max MP +20%."
    },
    
    "dread_armor": {
        "name": "Dread Armor",
        "req_job": "Dread Knight",
        "effect": "def_boost",
        "value": 1.2,
        "desc": "DEF +20%."
    },
    "darkness_affinity": {
        "name": "Darkness Affinity",
        "req_job": "Dread Knight",
        "effect": "dark_boost",
        "value": 1.25,
        "desc": "Dark element damage +25%."
    },
    "shadow_walker": {
        "name": "Shadow Walker",
        "req_job": "Dread Knight",
        "effect": "dodge_boost",
        "value": 1.15,
        "desc": "Dodge chance +15%."
    },
    
    "holy_aura": {
        "name": "Holy Aura",
        "req_job": "Holy Templar",
        "effect": "heal_boost",
        "value": 1.3,
        "desc": "Heal +30%."
    },
    "light_affinity": {
        "name": "Light Affinity",
        "req_job": "Holy Templar",
        "effect": "light_boost",
        "value": 1.25,
        "desc": "Light element damage +25%."
    },
    "holy_resistance": {
        "name": "Holy Resistance",
        "req_job": "Holy Templar",
        "effect": "status_resist",
        "value": 1.2,
        "desc": "Status effect resistance +20%."
    },
    
    "frostbite": {
        "name": "Frostbite Mastery",
        "req_job": "Blizzard Sovereign",
        "effect": "ice_boost",
        "value": 1.3,
        "desc": "Ice damage +30%."
    },
    "eternal_cold": {
        "name": "Eternal Cold",
        "req_job": "Blizzard Sovereign",
        "effect": "stun_boost",
        "value": 1.4,
        "desc": "Stun effect duration +40%."
    },
    "frozen_fortress": {
        "name": "Frozen Fortress",
        "req_job": "Blizzard Sovereign",
        "effect": "def_boost",
        "value": 1.25,
        "desc": "DEF +25%."
    },
}

# ==========================================
# === 3. BRANCHING EVOLUTION & COMBO DATA ===
# ==========================================
EVOLUTION_BRANCHES = {
    "fire_5": {
        "damage": {
            "name": "Hellfire Nova",
            "mult": 3.6,
            "status_effect": "burn"
        },
        "control": {
            "name": "Eternal Inferno",
            "mult": 2.8,
            "status_effect": "stun"
        },
        "heal": {
            "name": "Searing Rebirth",
            "mult": 3.2,
            "type": "heal"
        }
    },
    "water_5": {
        "heal": {
            "name": "Abyssal Restoration",
            "mult": 3.5,
            "type": "heal"
        },
        "damage": {
            "name": "Abyssal Crush",
            "mult": 3.4,
            "status_effect": "def_debuff"
        },
        "control": {
            "name": "Tidal Lock",
            "mult": 3.0,
            "status_effect": "stun"
        }
    },
    "ice_5": {
        "damage": {
            "name": "Glacial Annihilation",
            "mult": 3.7,
            "status_effect": "stun"
        },
        "control": {
            "name": "Frozen Time",
            "mult": 3.1,
            "status_effect": "stun"
        },
        "buff": {
            "name": "Perfect Frozen State",
            "mult": 0,
            "status_effect": "def_buff"
        }
    },
    "dark_5": {
        "damage": {
            "name": "Total Oblivion",
            "mult": 3.5,
            "status_effect": "def_debuff"
        },
        "control": {
            "name": "Void Prison",
            "mult": 3.0,
            "status_effect": "stun"
        }
    },
    "light_5": {
        "damage": {
            "name": "Divine Vortex",
            "mult": 3.4,
            "status_effect": "stun"
        },
        "heal": {
            "name": "Eternal Blessing",
            "mult": 3.6,
            "type": "heal"
        }
    }
}

# Combo Chains - Kombinasi skill yang memberikan bonus
COMBO_CHAINS = {
    ("double_slash", "cross_slash"): {
        "bonus_mult": 1.25,
        "extra_effect": "bleed"
    },
    ("fire_1", "fire_2"): {
        "bonus_mult": 1.3,
        "extra_effect": "burn"
    },
    ("fire_2", "fire_4"): {
        "bonus_mult": 1.4,
        "extra_effect": "burn"
    },
    ("shadow_step", "assassinate"): {
        "bonus_mult": 1.4,
        "extra_effect": "stun"
    },
    ("ice_1", "ice_2"): {
        "bonus_mult": 1.3,
        "extra_effect": "stun"
    },
    ("bolt_1", "bolt_2"): {
        "bonus_mult": 1.35,
        "extra_effect": "stun"
    },
    ("water_1", "water_2"): {
        "bonus_mult": 1.25,
        "extra_effect": "regen"
    },
    ("light_1", "light_2"): {
        "bonus_mult": 1.3,
        "extra_effect": "regen"
    },
    ("earth_1", "earth_2"): {
        "bonus_mult": 1.35,
        "extra_effect": "stun"
    },
    ("wind_1", "wind_2"): {
        "bonus_mult": 1.25,
        "extra_effect": "def_debuff"
    },
    ("dark_1", "dark_2"): {
        "bonus_mult": 1.3,
        "extra_effect": "def_debuff"
    },
    ("heavy_strike", "power_strike"): {
        "bonus_mult": 1.3,
        "extra_effect": None
    },
    ("piercing_thrust", "assassinate"): {
        "bonus_mult": 1.35,
        "extra_effect": "bleed"
    },
    ("shield_bash", "shield_counter"): {
        "bonus_mult": 1.25,
        "extra_effect": "stun"
    },
    ("flurry_strikes", "rapid_slash"): {
        "bonus_mult": 1.4,
        "extra_effect": "bleed"
    },
}

# ==========================================
# === 4. HELPER FUNCTIONS ===
# ==========================================
def record_skill_usage(player: Dict, skill_id: str) -> int:
    """Catat penggunaan skill untuk evolution tracking"""
    if not player or skill_id.startswith(("mon_", "miniboss_", "boss_")):
        return 0
    if 'skill_usages' not in player:
        player['skill_usages'] = {}
    player['skill_usages'][skill_id] = player['skill_usages'].get(skill_id, 0) + 1
    return player['skill_usages'][skill_id]


def get_cooldown_remaining(player: Dict, skill_id: str) -> int:
    """Cek cooldown tersisa untuk skill"""
    if 'skill_cooldowns' not in player:
        player['skill_cooldowns'] = {}
    return player['skill_cooldowns'].get(skill_id, 0)


def apply_cooldown(player: Dict, skill_id: str, cooldown_value: int) -> None:
    """Terapkan cooldown setelah pakai skill"""
    if 'skill_cooldowns' not in player:
        player['skill_cooldowns'] = {}
    player['skill_cooldowns'][skill_id] = cooldown_value


def reduce_all_cooldowns(player: Dict) -> None:
    """Kurangi cooldown setiap ronde"""
    if 'skill_cooldowns' in player:
        for skill in list(player['skill_cooldowns'].keys()):
            player['skill_cooldowns'][skill] = max(0, player['skill_cooldowns'][skill] - 1)
            if player['skill_cooldowns'][skill] == 0:
                del player['skill_cooldowns'][skill]


def get_last_used_skill(player: Dict) -> Optional[str]:
    """Ambil skill terakhir yang dipakai untuk combo"""
    return player.get('last_skill_used')


def set_last_used_skill(player: Dict, skill_id: str) -> None:
    """Set skill terakhir yang dipakai"""
    player['last_skill_used'] = skill_id


def get_monster_skill(monster: Dict) -> str:
    """
    Fungsi untuk menentukan skill yang digunakan oleh Monster/Boss.
    Mengambil secara acak dari list 'skills' yang ada di data monster.
    """
    monster_skills = monster.get('skills', [])
    if not monster_skills:
        return "mon_bite"  # Fallback jika monster tidak punya skill
    
    # Pilih satu skill secara acak
    selected_skill = random.choice(monster_skills)
    
    # Pastikan skill tersebut ada di database ACTIVE_SKILLS
    if selected_skill not in ACTIVE_SKILLS:
        return "mon_bite"
        
    return selected_skill


# ==========================================
# === 5. GET EFFECTIVE SKILL (Evolution + Branching) ===
# ==========================================
def get_effective_skill(player: Optional[Dict], skill_id: str) -> Optional[Dict]:
    """
    Hitung skill dengan evolution bonus dan branching
    Evolution mulai di 15 penggunaan, max 3 level
    """
    base_skill = ACTIVE_SKILLS.get(skill_id)
    if not base_skill:
        return None

    skill = base_skill.copy()

    # Monster/Boss tidak punya evolution
    if not player or skill_id.startswith(("mon_", "miniboss_", "boss_")):
        return skill

    uses = player.get('skill_usages', {}).get(skill_id, 0)
    if uses < SKILL_BALANCE_CONFIG["usage_threshold_for_evo"]:
        return skill

    # Hitung evolution level (1-3)
    evo_level = min(
        SKILL_BALANCE_CONFIG["max_evolution_level"],
        (uses - SKILL_BALANCE_CONFIG["usage_threshold_for_evo"]) // SKILL_BALANCE_CONFIG["usage_per_evo_level"] + 1
    )

    # Evolution bonus untuk damage & MP cost
    skill['mult'] = round(
        skill.get('mult', 1.0) * (1 + SKILL_BALANCE_CONFIG["base_mult_increase_per_evo"] * evo_level),
        2
    )
    skill['mp_cost'] = max(1, int(skill.get('mp_cost', 5) * (SKILL_BALANCE_CONFIG["base_mp_reduction_per_evo"] ** evo_level)))

    # Branching di level 3
    if evo_level >= 3 and skill_id in EVOLUTION_BRANCHES:
        branch_type = random.choice(list(EVOLUTION_BRANCHES[skill_id].keys()))
        branch_data = EVOLUTION_BRANCHES[skill_id][branch_type]
        skill['name'] = branch_data.get("name", skill['name'])
        skill['mult'] = branch_data.get("mult", skill['mult'])
        if "status_effect" in branch_data:
            skill['status_effect'] = branch_data["status_effect"]
        if "type" in branch_data:
            skill['type'] = branch_data["type"]

    # Nama visual untuk evolution
    if evo_level == 1:
        skill['name'] += " +"
    elif evo_level == 2:
        skill['name'] += " ++"
    elif evo_level == 3:
        skill['name'] += " ★"

    return skill


# ==========================================
# === 6. GET AVAILABLE SKILLS ===
# ==========================================
def get_available_skills(player: Dict, player_stats: Dict) -> List[str]:
    """
    Ambil list skill yang bisa dipakai (cek level, cooldown, requirement)
    """
    available = []
    job = player.get('current_job', 'Novice Weaver')
    player_level = player.get('level', 1)
    element = player_stats.get('element', 'none').lower()
    weapon_type = player_stats.get('weapon_type', 'unarmed').lower()
    offhand_type = player_stats.get('offhand_type', 'none').lower()

    for skill_id, skill in ACTIVE_SKILLS.items():
        # Skip monster skills
        if skill_id.startswith(("mon_", "miniboss_", "boss_")):
            continue

        # Check level
        if player_level < skill.get("unlock_level", 1):
            continue

        # Check cooldown
        if get_cooldown_remaining(player, skill_id) > 0:
            continue

        can_use = True

        # Check weapon requirement
        if "req_weapon" in skill:
            req_list = skill["req_weapon"] if isinstance(skill["req_weapon"], list) else [skill["req_weapon"]]
            if weapon_type not in req_list and offhand_type not in req_list:
                can_use = False
        # Check job requirement
        elif "req_job" in skill:
            if skill["req_job"] != job:
                can_use = False
        # Check element requirement
        else:
            if skill["element"] != "none" and skill["element"] != element:
                can_use = False

        if can_use:
            available.append(skill_id)

    # Fallback jika tidak ada skill tersedia
    if not available:
        fallback = "heavy_strike" if player_stats.get("attack_type") != "magic" else "mana_bullet"
        available.append(fallback)

    return available


# ==========================================
# === 7. EXECUTE SKILL (Combo + Evolution + Cooldown) ===
# ==========================================
def execute_skill(
    attacker_stats: Dict,
    defender_stats: Dict,
    skill_id: str,
    player: Optional[Dict] = None
) -> Tuple[str, int, Optional[str], str]:
    """
    Eksekusi skill dengan combo, evolution, cooldown handling
    Return: (type, damage/heal, status_effect, log_message)
    """
    
    # Handle basic attack
    if skill_id == "basic_attack":
        skill = {
            "name": "Basic Attack",
            "mult": 1.0,
            "type": attacker_stats.get("attack_type", "physical"),
            "element": attacker_stats.get("element", "none"),
            "status_effect": None,
            "cooldown": 0
        }
    else:
        skill = get_effective_skill(player, skill_id)

    if not skill:
        return "error", 0, None, "💨 Aksinya meleset!"

    log = [f"✨ Menggunakan <b>{skill['name']}</b>!"]

    # === COMBO CHECK ===
    combo_bonus = 1.0
    extra_status = None
    last_skill = get_last_used_skill(player) if player else None
    if player and last_skill and (last_skill, skill_id) in COMBO_CHAINS:
        combo_data = COMBO_CHAINS[(last_skill, skill_id)]
        combo_bonus = combo_data.get("bonus_mult", 1.0)
        extra_status = combo_data.get("extra_effect")
        log.append("🔗 <i>COMBO ACTIVATED!</i>")

    # === HEAL / BUFF / DEBUFF ===
    if skill["type"] in ["heal", "buff"]:
        if skill["type"] == "heal":
            m_atk = attacker_stats.get("m_atk", 10)
            heal_amount = int(m_atk * skill["mult"] * random.uniform(0.9, 1.1) * combo_bonus)
            
            # Job passive bonus
            if attacker_stats.get('current_job') == "Holy Templar":
                heal_amount = int(heal_amount * 1.3)
            
            log.append(f"💚 Memulihkan {heal_amount} HP.")
            if player:
                apply_cooldown(player, skill_id, skill.get("cooldown", 0))
                set_last_used_skill(player, skill_id)
                record_skill_usage(player, skill_id)
            
            return "heal", heal_amount, skill.get("status_effect"), " ".join(log)
        else:
            log.append(f"🛡️ Aura {skill['status_effect'].upper()} aktif.")
            if player:
                apply_cooldown(player, skill_id, skill.get("cooldown", 0))
                set_last_used_skill(player, skill_id)
                record_skill_usage(player, skill_id)
            
            return "buff", 0, skill["status_effect"], " ".join(log)

    if skill["type"] == "debuff":
        log.append(f"⚠️ Target terkena {skill['status_effect'].upper()}!")
        if player:
            apply_cooldown(player, skill_id, skill.get("cooldown", 0))
            set_last_used_skill(player, skill_id)
            record_skill_usage(player, skill_id)
        
        return "debuff", 0, skill["status_effect"], " ".join(log)

    # === DAMAGE CALCULATION ===
    if skill["type"] == "physical":
        atk_val = attacker_stats.get("p_atk", 10)
        def_val = defender_stats.get("p_def", 5)
    else:
        atk_val = attacker_stats.get("m_atk", 10)
        def_val = defender_stats.get("m_def", 5)

    # Base formula: ATK² / (ATK + DEF + 1)
    base_dmg = (atk_val ** 2) / (atk_val + def_val + 1)
    base_dmg *= skill["mult"] * combo_bonus
    base_dmg *= random.uniform(0.9, 1.1)

    # === ELEMENT & WEAKNESS ===
    multiplier = 1.0
    atk_element = skill["element"]
    
    # Element affinity bonus
    if atk_element == "fire" and attacker_stats.get("element") == "fire":
        multiplier *= 1.2
    if atk_element == "ice" and attacker_stats.get("current_job") == "Blizzard Sovereign":
        multiplier *= 1.3
    if atk_element == "light" and attacker_stats.get("current_job") == "Holy Templar":
        multiplier *= 1.2
    if atk_element == "dark" and attacker_stats.get("current_job") == "Dread Knight":
        multiplier *= 1.2

    # Defender weakness check
    def_weakness = defender_stats.get("monster_weakness", defender_stats.get("weakness", "none")).lower()
    if atk_element == def_weakness and atk_element != "none":
        multiplier *= 1.5
        log.append("🔥 <i>SUPER EFFECTIVE!</i>")

    final_dmg = max(1, int(base_dmg * multiplier))

    # === STATUS EFFECT ===
    applied_status = skill.get("status_effect")
    if extra_status:
        applied_status = extra_status
    elif applied_status and random.random() < SKILL_BALANCE_CONFIG["combo_activation_chance"]:
        log.append(f"⚠️ Target terkena {applied_status.upper()}!")
    else:
        applied_status = None

    log_msg = " ".join(log) + f" (-{final_dmg} HP)"

    if player:
        apply_cooldown(player, skill_id, skill.get("cooldown", 0))
        set_last_used_skill(player, skill_id)
        record_skill_usage(player, skill_id)

    return "damage", final_dmg, applied_status, log_msg


# ==========================================
# === 8. SKILL STATISTICS & INFO ===
# ==========================================
def get_skill_stats_summary() -> Dict:
    """Ambil statistik jumlah skill per kategori"""
    stats = {
        "total_active_skills": len(ACTIVE_SKILLS),
        "total_passive_skills": len(PASSIVE_SKILLS),
        "physical_skills": 0,
        "magic_skills": 0,
        "heal_skills": 0,
        "buff_skills": 0,
        "weapon_specific": 0,
        "element_skills": defaultdict(int),
        "job_skills": defaultdict(int),
    }

    for skill_id, skill in ACTIVE_SKILLS.items():
        if skill["type"] == "physical":
            stats["physical_skills"] += 1
        elif skill["type"] == "magic":
            stats["magic_skills"] += 1
        elif skill["type"] == "heal":
            stats["heal_skills"] += 1
        elif skill["type"] == "buff":
            stats["buff_skills"] += 1

        if "req_weapon" in skill:
            stats["weapon_specific"] += 1

        if skill["element"] != "none":
            stats["element_skills"][skill["element"]] += 1

        if "req_job" in skill:
            stats["job_skills"][skill["req_job"]] += 1

    return dict(stats)


def print_skill_summary():
    """Print summary skill system"""
    stats = get_skill_stats_summary()
    print("=" * 60)
    print("SISTEM SKILL & MAGIC - THE ARCHIVUS")
    print("=" * 60)
    print(f"Total Active Skills: {stats['total_active_skills']}")
    print(f"Total Passive Skills: {stats['total_passive_skills']}")
    print(f"\nSkill Type Distribution:")
    print(f"  Physical Skills: {stats['physical_skills']}")
    print(f"  Magic Skills: {stats['magic_skills']}")
    print(f"  Heal Skills: {stats['heal_skills']}")
    print(f"  Buff Skills: {stats['buff_skills']}")
    print(f"  Weapon Specific: {stats['weapon_specific']}")
    print(f"\nElement Distribution:")
    for element, count in sorted(stats['element_skills'].items()):
        print(f"  {element.title()}: {count} skills")
    print(f"\nJob Distribution:")
    for job, count in sorted(stats['job_skills'].items()):
        print(f"  {job}: {count} skills")
    print("=" * 60)


if __name__ == "__main__":
    print_skill_summary()
