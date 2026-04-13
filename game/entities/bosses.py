"""
Database Bos dan Mini-Bos Archivus
"""
import random

BOSS_NAMES = [
    "THE KEEPER", 
    "JAMES MARCUS ECHO", 
    "VOID OVERLORD", 
    "THE FINAL ARCHIVIST", 
    "ORPHAN OF THE ARCHIVES"
]

def get_random_boss():
    """Mengambil nama bos acak"""
    return random.choice(BOSS_NAMES)
