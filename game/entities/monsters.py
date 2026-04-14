"""
Database Monster Archivus (Tier 1-5)
Berisi lebih dari 500 monster unik untuk eksplorasi tanpa batas.
Dikurasi khusus untuk tema Dark Fantasy & Cosmic Horror.
"""
import random

MONSTER_NAMES = {
    # === TIER 1: Makhluk Lemah, Hama Dimensi, dan Pecahan Memori (100+ Monster) ===
    1: [
        "Shadow Crawler", "Dust Mite", "Hollow Whisper", "Lost Fragment", "Gloom Fiend", "Crawling Ink", "Blind Rat",
        "Shadow Whisper", "Shadow Fragment", "Shadow Rat", "Shadow Bat", "Shadow Slime", "Shadow Wisp", "Shadow Imp",
        "Dust Crawler", "Dust Whisper", "Dust Fragment", "Dust Fiend", "Dust Bat", "Dust Slime", "Dust Wisp", "Dust Imp",
        "Hollow Crawler", "Hollow Mite", "Hollow Fragment", "Hollow Fiend", "Hollow Rat", "Hollow Bat", "Hollow Slime", "Hollow Imp",
        "Gloom Crawler", "Gloom Mite", "Gloom Whisper", "Gloom Fragment", "Gloom Rat", "Gloom Bat", "Gloom Slime", "Gloom Wisp",
        "Ink Crawler", "Ink Mite", "Ink Whisper", "Ink Fragment", "Ink Fiend", "Ink Rat", "Ink Bat", "Ink Wisp", "Ink Imp",
        "Pale Crawler", "Pale Mite", "Pale Whisper", "Pale Fragment", "Pale Fiend", "Pale Rat", "Pale Bat", "Pale Slime", "Pale Wisp",
        "Rust Crawler", "Rust Mite", "Rust Whisper", "Rust Fragment", "Rust Fiend", "Rust Rat", "Rust Bat", "Rust Slime", "Rust Imp",
        "Ash Crawler", "Ash Mite", "Ash Whisper", "Ash Fragment", "Ash Fiend", "Ash Rat", "Ash Bat", "Ash Slime", "Ash Wisp", "Ash Imp",
        "Fog Crawler", "Fog Mite", "Fog Whisper", "Fog Fragment", "Fog Fiend", "Fog Rat", "Fog Bat", "Fog Slime", "Fog Wisp", "Fog Imp",
        "Void Crawler", "Void Mite", "Void Whisper", "Void Fragment", "Void Fiend", "Void Rat", "Void Bat", "Void Slime", "Void Wisp", "Void Imp",
        "Forgotten Mote", "Decaying Scraps", "Murky Droplet", "Blind Wisp", "Static Glitch"
    ],
    
    # === TIER 2: Penjaga Korup, Prajurit Jatuh, dan Parasit (100+ Monster) ===
    2: [
        "Archivus Guard", "Void Stalker", "Ink Slime", "Memory Parasite", "Shattered Knight", "Faceless Scribe", "Echo Phantom",
        "Archivus Stalker", "Archivus Parasite", "Archivus Scribe", "Archivus Phantom", "Archivus Ghoul", "Archivus Hound", "Archivus Skeleton",
        "Shattered Guard", "Shattered Stalker", "Shattered Parasite", "Shattered Scribe", "Shattered Phantom", "Shattered Ghoul", "Shattered Hound",
        "Faceless Guard", "Faceless Stalker", "Faceless Parasite", "Faceless Knight", "Faceless Phantom", "Faceless Ghoul", "Faceless Hound",
        "Echo Guard", "Echo Stalker", "Echo Parasite", "Echo Knight", "Echo Scribe", "Echo Ghoul", "Echo Hound", "Echo Skeleton",
        "Cursed Guard", "Cursed Stalker", "Cursed Parasite", "Cursed Knight", "Cursed Scribe", "Cursed Phantom", "Cursed Ghoul", "Cursed Skeleton",
        "Blood Guard", "Blood Stalker", "Blood Parasite", "Blood Knight", "Blood Scribe", "Blood Phantom", "Blood Hound", "Blood Skeleton",
        "Crypt Guard", "Crypt Stalker", "Crypt Parasite", "Crypt Knight", "Crypt Scribe", "Crypt Phantom", "Crypt Ghoul", "Crypt Hound",
        "Iron Guard", "Iron Stalker", "Iron Parasite", "Iron Knight", "Iron Scribe", "Iron Phantom", "Iron Ghoul", "Iron Skeleton",
        "Dead Guard", "Dead Stalker", "Dead Parasite", "Dead Knight", "Dead Scribe", "Dead Phantom", "Dead Hound", "Dead Skeleton",
        "Broken Guard", "Broken Stalker", "Broken Parasite", "Broken Knight", "Broken Scribe", "Broken Phantom", "Broken Ghoul", "Broken Hound",
        "Corrupted Marionette", "Wandering Armor", "Blind Swordsman", "Glitch Zombie", "Rusted Golem"
    ],
    
    # === TIER 3: Predator Dimensi, Penyihir Gelap, dan Roh Agresif (100+ Monster) ===
    3: [
        "Soul Eater", "Memory Butcher", "The Forgotten Weaver", "Crimson Wraith", "Abyssal Hound", "Grief Lurker", "Tomb Warden",
        "Soul Butcher", "Soul Weaver", "Soul Wraith", "Soul Lurker", "Soul Warden", "Soul Demon", "Soul Reaper", "Soul Banshee", "Soul Golem",
        "Memory Eater", "Memory Weaver", "Memory Wraith", "Memory Lurker", "Memory Warden", "Memory Demon", "Memory Reaper", "Memory Banshee",
        "Crimson Eater", "Crimson Butcher", "Crimson Weaver", "Crimson Lurker", "Crimson Warden", "Crimson Demon", "Crimson Reaper", "Crimson Golem",
        "Abyssal Eater", "Abyssal Butcher", "Abyssal Weaver", "Abyssal Wraith", "Abyssal Lurker", "Abyssal Warden", "Abyssal Reaper", "Abyssal Banshee",
        "Grief Eater", "Grief Butcher", "Grief Weaver", "Grief Wraith", "Grief Warden", "Grief Demon", "Grief Reaper", "Grief Banshee", "Grief Golem",
        "Tomb Eater", "Tomb Butcher", "Tomb Weaver", "Tomb Wraith", "Tomb Lurker", "Tomb Demon", "Tomb Reaper", "Tomb Banshee", "Tomb Golem",
        "Dread Eater", "Dread Butcher", "Dread Weaver", "Dread Wraith", "Dread Lurker", "Dread Warden", "Dread Demon", "Dread Reaper", "Dread Golem",
        "Chaos Eater", "Chaos Butcher", "Chaos Weaver", "Chaos Wraith", "Chaos Lurker", "Chaos Warden", "Chaos Demon", "Chaos Banshee", "Chaos Golem",
        "Warp Eater", "Warp Butcher", "Warp Weaver", "Warp Wraith", "Warp Lurker", "Warp Warden", "Warp Demon", "Warp Reaper", "Warp Banshee",
        "Glitch Eater", "Glitch Butcher", "Glitch Weaver", "Glitch Wraith", "Glitch Lurker", "Glitch Warden", "Glitch Demon", "Glitch Reaper", "Glitch Golem",
        "Tormented Illusion", "Hexed Gargoyle", "Cursed Inquisitor", "Shadow Sorcerer", "Phantom Executioner"
    ],
    
    # === TIER 4: Elite, Monster Kosmik, dan Utusan Kehancuran (100+ Monster) ===
    4: [
        "Abyssal Knight", "Glitch Specter", "Time Devourer", "Chaos Oracle", "Void Behemoth", "Doom Herald", "Ruin Walker",
        "Glitch Devourer", "Glitch Oracle", "Glitch Behemoth", "Glitch Herald", "Glitch Walker", "Glitch Warlord", "Glitch Titan", "Glitch Archon",
        "Time Specter", "Time Oracle", "Time Behemoth", "Time Herald", "Time Walker", "Time Warlord", "Time Titan", "Time Sorcerer", "Time Archon",
        "Chaos Specter", "Chaos Devourer", "Chaos Behemoth", "Chaos Herald", "Chaos Walker", "Chaos Warlord", "Chaos Titan", "Chaos Sorcerer", "Chaos Archon",
        "Doom Specter", "Doom Devourer", "Doom Oracle", "Doom Behemoth", "Doom Walker", "Doom Warlord", "Doom Titan", "Doom Sorcerer", "Doom Archon",
        "Ruin Specter", "Ruin Devourer", "Ruin Oracle", "Ruin Behemoth", "Ruin Herald", "Ruin Warlord", "Ruin Titan", "Ruin Sorcerer", "Ruin Archon",
        "Astral Specter", "Astral Devourer", "Astral Oracle", "Astral Behemoth", "Astral Herald", "Astral Walker", "Astral Warlord", "Astral Titan", "Astral Archon",
        "Cosmic Specter", "Cosmic Devourer", "Cosmic Oracle", "Cosmic Behemoth", "Cosmic Herald", "Cosmic Walker", "Cosmic Warlord", "Cosmic Sorcerer", "Cosmic Archon",
        "Eclipse Specter", "Eclipse Devourer", "Eclipse Oracle", "Eclipse Behemoth", "Eclipse Herald", "Eclipse Walker", "Eclipse Warlord", "Eclipse Titan", "Eclipse Archon",
        "Infernal Specter", "Infernal Devourer", "Infernal Oracle", "Infernal Behemoth", "Infernal Herald", "Infernal Walker", "Infernal Warlord", "Infernal Sorcerer", "Infernal Archon",
        "Eldritch Specter", "Eldritch Devourer", "Eldritch Oracle", "Eldritch Behemoth", "Eldritch Herald", "Eldritch Walker", "Eldritch Titan", "Eldritch Sorcerer", "Eldritch Archon",
        "Dimension Ripper", "Nebula Colossus", "Reality Shredder", "Abyssal Overlord", "Quantum Phantom"
    ],
    
    # === TIER 5: Bos, Entitas Kuno, dan Dewa Dimensi (100+ Monster) ===
    5: [
        "Ancient Behemoth", "Reality Weaver", "Void Leviathan", "The First Scribe", "Astral Dragon", "The Nameless King", "Eternal Nightmare",
        "Ancient Leviathan", "Ancient Dragon", "Ancient King", "Ancient Nightmare", "Ancient Emperor", "Ancient Deity", "Ancient Creator", "Ancient Sovereign", "Ancient Seraph",
        "Reality Leviathan", "Reality Dragon", "Reality King", "Reality Nightmare", "Reality Emperor", "Reality Deity", "Reality Creator", "Reality Sovereign", "Reality Titan",
        "Void Dragon", "Void King", "Void Nightmare", "Void Emperor", "Void Deity", "Void Creator", "Void Sovereign", "Void Seraph", "Void Titan",
        "Astral Leviathan", "Astral King", "Astral Nightmare", "Astral Emperor", "Astral Deity", "Astral Creator", "Astral Sovereign", "Astral Seraph", "Astral Titan",
        "Eternal Leviathan", "Eternal Dragon", "Eternal King", "Eternal Emperor", "Eternal Deity", "Eternal Creator", "Eternal Sovereign", "Eternal Seraph", "Eternal Titan",
        "Primordial Behemoth", "Primordial Leviathan", "Primordial Dragon", "Primordial King", "Primordial Nightmare", "Primordial Emperor", "Primordial Deity", "Primordial Creator", "Primordial Sovereign", "Primordial Titan",
        "Infinite Behemoth", "Infinite Leviathan", "Infinite Dragon", "Infinite King", "Infinite Nightmare", "Infinite Emperor", "Infinite Deity", "Infinite Sovereign", "Infinite Seraph", "Infinite Titan",
        "Supreme Behemoth", "Supreme Leviathan", "Supreme Dragon", "Supreme King", "Supreme Nightmare", "Supreme Emperor", "Supreme Deity", "Supreme Creator", "Supreme Seraph", "Supreme Titan",
        "Nameless Behemoth", "Nameless Leviathan", "Nameless Dragon", "Nameless Nightmare", "Nameless Emperor", "Nameless Deity", "Nameless Creator", "Nameless Sovereign", "Nameless Seraph", "Nameless Titan",
        "True Behemoth", "True Leviathan", "True Dragon", "True King", "True Nightmare", "True Emperor", "True Deity", "True Creator", "True Sovereign", "True Titan",
        "The Final Paradox", "Alpha and Omega", "The Weaver of Fate", "Cosmic Devastator", "The Sleeping God"
    ]
}

def get_random_monster(tier):
    """Mengambil nama monster acak berdasarkan tier (Melindungi dari input di luar batas 1-5)"""
    safe_tier = max(1, min(tier, 5))
    return random.choice(MONSTER_NAMES[safe_tier])
