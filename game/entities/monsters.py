"""
Database Monster Archivus (Tier 1-5)
"""
import random

MONSTER_NAMES = {
    1: ["Shadow Crawler", "Dust Mite", "Hollow Whisper", "Lost Fragment", "Gloom Fiend", "Crawling Ink", "Blind Rat"],
    2: ["Archivus Guard", "Void Stalker", "Ink Slime", "Memory Parasite", "Shattered Knight", "Faceless Scribe", "Echo Phantom"],
    3: ["Soul Eater", "Memory Butcher", "The Forgotten Weaver", "Crimson Wraith", "Abyssal Hound", "Grief Lurker", "Tomb Warden"],
    4: ["Abyssal Knight", "Glitch Specter", "Time Devourer", "Chaos Oracle", "Void Behemoth", "Doom Herald", "Ruin Walker"],
    5: ["Ancient Behemoth", "Reality Weaver", "Void Leviathan", "The First Scribe", "Astral Dragon", "The Nameless King", "Eternal Nightmare"]
}

def get_random_monster(tier):
    """Mengambil nama monster acak berdasarkan tier"""
    safe_tier = min(tier, 5)
    return random.choice(MONSTER_NAMES[safe_tier])
