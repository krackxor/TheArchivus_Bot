# game/items/masks.py

MASKS = {
    "frozen_visage": {
        "id": "frozen_visage", "name": "Frozen Visage", "tier": 4,
        "m_atk": 10, "resist": ["burn"], "weight": 2,
        "description": "Topeng es yang membekukan emosi pemakainya."
    },
    "eagle_eye_monocle": {
        "id": "eagle_eye_monocle", "name": "Eagle-Eye Monocle", "tier": 4,
        "accuracy": 30, "crit_chance": 0.15, "weight": 1,
        "description": "Lensa presisi tinggi untuk membidik titik fatal. Syarat Phantom Archer."
    },
    "plague_doctor_mask": {
        "id": "plague_doctor_mask", "name": "Plague Doctor Mask", "tier": 4,
        "resist": ["poison", "infection"], "weight": 2,
        "description": "Paruh burung berisi rempah penolak wabah. Syarat Blood Reaper & Alchemist."
    },
    "ancient_mask": {
        "id": "ancient_mask", "name": "The Ancient Mask", "tier": 5,
        "p_atk": 5, "m_atk": 5, "speed": 5, "weight": 0,
        "description": "Topeng tanpa wajah. Hanya untuk mereka yang berani menjadi 'The Faceless'."
    }
}
