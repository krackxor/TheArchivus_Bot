import random
from database import get_random_narrative

NPC_NAMES = ["The Wanderer", "Hollow Sentinel", "Echo of Silence", "Pale Weaver", "Blind Scholar"]
NPC_TRAITS = ["Gemetar", "Tenang", "Sinis", "Melankolis", "Marah"]

def generate_npc(is_liar=False):
    name = random.choice(NPC_NAMES)
    trait = random.choice(NPC_TRAITS)
    reason = "npc_lie" if is_liar else "npc_honest"
    dialog = get_random_narrative(category="npc_dialog", reason=reason)
    
    return {
        "identity": f"{name} yang {trait}",
        "is_liar": is_liar,
        "dialog": dialog
    }

def get_death_message(cause):
    return get_random_narrative(category="death_note", reason=cause)
