# game/consumables/special.py

"""
Database Special Items
Berisi item unik yang memiliki fungsi khusus di luar ramuan dan alat kemah.
"""

SPECIAL_ITEMS = {
    # Contoh jika nanti kamu butuh item khusus:
    # "ancient_scroll": {
    #     "id": "ancient_scroll",
    #     "name": "Gulungan Kuno",
    #     "type": "consumable",
    #     "effect_type": "trigger_quiz",
    #     "description": "Gulungan tua berisi teka-teki kuno.",
    #     "tier": 2
    # }
}

def get_item(item_id):
    return SPECIAL_ITEMS.get(item_id)
