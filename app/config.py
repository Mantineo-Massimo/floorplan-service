"""
EN: Loads and parses configuration from environment variables.
IT: Carica ed effettua il parsing della configurazione dalle variabili d'ambiente.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# EN: Parse the comma-separated BUILDING string into a dictionary.
# IT: Esegue il parsing della stringa BUILDING separata da virgole in un dizionario.
buildings_str = os.getenv("BUILDINGS", "A:building_A,B:building_B,SBA:building_SBA")
BUILDING_PATHS = {
    key.strip(): val.strip()
    for item in buildings_str.split(',')
    for key, val in [item.split(':')]
}

# EN: Parse the comma-separated FLOORS string into a set of integers.
# IT: Esegue il parsing della stringa FLOORS separata da virgole in un set di interi.
floors_str = os.getenv("ALLOWED_FLOORS", "-1,0,1,2,3")
ALLOWED_FLOORS = {int(floor.strip()) for floor in floors_str.split(',')}

# EN: Load Redis URL and Cache TTL from environment.
# IT: Carica l'URL di Redis e il TTL della cache dall'ambiente.
REDIS_URL = os.getenv("REDIS_URL", "redis://redis_cache:6379/0")
CACHE_TTL_MINUTES = int(os.getenv("CACHE_TTL_MINUTES", 60))