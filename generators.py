import random
from database import get_random_narrative

# DNA Suku Cadang NPC (Bisa kamu tambah terus nanti)
NPC_NAMES = ["The Wanderer", "Hollow Sentinel", "Echo of Silence", "Pale Weaver", "Blind Scholar", "Dust Phantom"]
NPC_TRAITS = ["Gemetar", "Tenang", "Sinis", "Melankolis", "Marah", "Tersenyum Pucat"]

def generate_npc(is_liar=False):
    """
    Merakit entitas NPC secara dinamis (Nama + Sifat + Dialog).
    Hasilnya tidak akan pernah sama persis.
    """
    name = random.choice(NPC_NAMES)
    trait = random.choice(NPC_TRAITS)
    
    # Ambil dialog dari MongoDB (1.000 list tadi)
    reason = "npc_lie" if is_liar else "npc_honest"
    dialog = get_random_narrative(category="npc_dialog", reason=reason)
    
    return {
        "identity": f"{name} yang {trait}",
        "is_liar": is_liar,
        "dialog": dialog
    }

def get_death_message(cause):
    """
    Mengambil pesan kematian yang pas.
    cause: 'death_trap' (tertipu), 'death_combat' (kalah), 'death_timeout' (waktu habis)
    """
    return get_random_narrative(category="death_note", reason=cause)
