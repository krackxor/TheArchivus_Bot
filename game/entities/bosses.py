"""
Database Bos dan Mini-Bos Archivus
Masing-masing kategori berisi 100 entitas unik.
Dirancang khusus dengan tema Dark Fantasy, Cosmic Horror, dan Easter Egg Sci-Fi.
"""
import random

# === DAFTAR 100 MINI-BOS (Mid-Encounter Threats) ===
MINI_BOSS_NAMES = [
    "Shadow Sentinel", "Ink Lieutenant", "Hollow Commander", "Void Skirmisher", "Memory Glitch",
    "Cursed Captain", "Echo Stalker", "Dust Overseer", "Broken Knight", "Fragmented Soul",
    "Gloom Herald", "Pale Inquisitor", "Corrupted Scribe", "Shattered Guard", "Blighted Weaver",
    "Silent Executioner", "Vengeful Echo", "Deep Sea Parasite", "Arklay Survivor", "Umbrella Trainee",
    "Lesser Chimera", "Flesh Golem", "Bone Warden", "Static Phantom", "Rusted Centurion",
    "Neural Devourer", "Sorrow Crawler", "Regret Weaver", "Agony Shard", "Twisted Mentor",
    "Void Assassin", "Dimensional Ripper", "Time Leech", "Event Shadow", "Nebula Wisp",
    "Gravity Anomaly", "Aether Stalker", "Quantum Wraith", "Binary Specter", "Logic Breaker",
    "Obsidian Gargoyle", "Crimson Guard", "Infernal Scout", "Abyssal Monk", "Nightmare Larva",
    "Dream Fragment", "Subconscious Terror", "Amnesia Wraith", "Forgotten Pawn", "Hidden Blade",
    "The Weeping Statue", "Mirror Doppelganger", "Glass Stalker", "Crystal Fiend", "Sand Wanderer",
    "Ash Revenant", "Pyre Walker", "Frost Ghost", "Storm Harbinger", "Volt Lurker",
    "Toxic Chemist", "Plague Doctor Echo", "Venom Spitter", "Acid Slime Lord", "Bio-Weapon Beta",
    "Hunter Gamma Shadow", "Tyrant Prototype", "Zombie Alpha Commander", "Leech Swarm Heart", "Web Weaver",
    "Iron Maiden Echo", "Executioner Majini Shadow", "Chainsaw Villager Soul", "Plaga Apostle", "Verdugo Larva",
    "Blade of Archivus", "Shield of Memories", "Spear of Oblivion", "Bow of Silence", "Dagger of Deceit",
    "The Lone Wolf", "The Cursed Squire", "The Fallen Monk", "The Mad Artist", "The Blind Musician",
    "The Silent Librarian", "The Clockwork Toy", "The Rusty Automaton", "The Steam Juggernaut", "The Gear Grinder",
    "Lesser Lich", "Wraith King Apprentice", "Mini Behemoth", "Baby Dragon", "Void Jellyfish",
    "The Ink Blot", "The Paper Cut", "The Scribbled Horror", "The Eraser", "The Inkwell Demon"
]

# === DAFTAR 100 BOS UTAMA (End-Cycle Overlords) ===
BOSS_NAMES = [
    "THE KEEPER", "JAMES MARCUS ECHO", "VOID OVERLORD", "THE FINAL ARCHIVIST", "ORPHAN OF THE ARCHIVES",
    "ALBERT WESKER PHANTOM", "NEMESIS PRIME", "SEPHIROTH'S SHADOW", "THE FIRST WEAVER", "ARCHIVUS PRIME",
    "CHRONOS DEVOURER", "ASTRAL DICTATOR", "THE INFINITE PARADOX", "CLOCKWORK LEVIATHAN", "DIMENSION SHREDDER",
    "ECLIPSE SOVEREIGN", "THE TIMELESS KING", "WARP OVERLORD", "NEBULA TYRANT", "THE EVENT HORIZON",
    "GRAVITY BENDER", "REALITY FRACTURE", "THE ASTRAL JUDGE", "CHRONO WARDEN", "THE VOID WALKER",
    "ETERNITY'S END", "THE COSMIC ANOMALY", "SINGULARITY PRIME", "THE ASTRAL FORGER", "THE TIMELESS ORACLE",
    "THE MEMORY THIEF PRIME", "OBLIVION SCRIBE", "THE HOLLOW MIND", "EATER OF REGRETS", "THE FORGOTTEN SOVEREIGN",
    "ILLUSION GRANDMASTER", "THE SHATTERED PSYCHE", "NIGHTMARE INCARNATE", "THE DREAM EATER", "COGNITIVE ANOMALY",
    "THE LOST EMPEROR", "AMNESIA LORD", "THE MIND FLAYER", "PHANTOM OF REGRET", "THE SILENT SCREAM",
    "THE ECHOING VOID", "MEMORY'S END", "THE MAD SCHOLAR", "THE CORRUPTED ORACLE", "THE BLIND PROPHET",
    "CRIMSON BEHEMOTH", "ABYSSAL WARLORD", "THE BLOOD KING", "CORRUPTED SERAPH", "THE FALLEN PALADIN",
    "DOOMBRINGER", "RUIN INCARNATE", "THE ASHEN LORD", "PLAGUE BRINGER", "THE RUSTED TITAN",
    "BONE EMPEROR", "THE FLESH CRAFTER", "SHADOW BEHEMOTH", "THE GLOOM SOVEREIGN", "INK LEVIATHAN",
    "THE PALE DUKE", "TERROR INCARNATE", "THE HOLLOWED KING", "BANE OF ARKLAY", "THE DARK MESSIAH",
    "ABYSSAL LEVIATHAN", "THE CURSED MONARCH", "THE SOULLESS KNIGHT", "THE DESPAIR BRINGER", "THE VOID DRAGON",
    "THE NAMELESS GOD", "OMEGA ENTITY", "THE ALPHA CONSTRUCT", "CELESTIAL TITAN", "THE STAR EATER",
    "VOID SERAPH", "THE SUPREME ARCHITECT", "THE FINAL JUDGMENT", "GALACTIC OVERLORD", "THE ENDLESS ABYSS",
    "THE COSMIC PARADOX", "THE UNSEEN TERROR", "THE SILENT GOD", "THE ETERNAL EMPEROR", "THE FIRST CAUSE",
    "THE LAST EFFECT", "THE VOID INCARNATE", "THE ASTRAL LEVIATHAN", "THE NEBULA KING", "THE QUASAR TITAN",
    "THE BLACK HOLE ENTITY", "THE DIMENSIONAL DEVOURER", "THE FABRIC TEARER", "THE WEAVER OF ENDINGS", "THE ULTIMATE TRUTH"
]

def get_random_mini_boss():
    """Mengambil nama mini-bos acak."""
    return random.choice(MINI_BOSS_NAMES)

def get_random_boss():
    """Mengambil nama bos utama acak."""
    return random.choice(BOSS_NAMES)
