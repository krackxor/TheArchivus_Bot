# game/systems/narrative.py
from game.data.script import DESPAIR_STEPS, MONSTER_WARNINGS
import random

def get_step_narration(step_count):
    """Mengambil narasi linear berdasarkan langkah pemain"""
    # Menggunakan get() agar jika langkah > daftar yang ada, tidak error
    text = DESPAIR_STEPS.get(step_count)
    
    if not text:
        # Jika langkah sudah melewati batas script, gunakan looping atau fallback
        fallback_idx = (step_count % len(DESPAIR_STEPS)) + 1
        text = DESPAIR_STEPS.get(fallback_idx, "Kegelapan ini mulai bosan melihatmu.")
        
    return f"👣 **Langkah {step_count}**\n_{text}_"

def get_monster_warning():
    """Mengambil peringatan monster secara acak untuk efek kejutan"""
    return f"👹 **{random.choice(MONSTER_WARNINGS)}**"
