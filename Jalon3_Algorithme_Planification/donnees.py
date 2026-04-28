import math

# Coordonnées GPS (latitude, longitude) de chaque site - EPSG:4326
DELIVERY_SITES_GPS = {
    'Parc_Citadelle': (50.631, 3.053),  # Point de départ/base (approximation)
    'ONERA': (50.603, 3.091),
    'CHU_Lille': (50.581, 3.057),
    'Aerodrome_Marcq': (50.682, 3.081),
    'Grand_Palais': (50.603, 3.089),
    'EuraTechnologies': (50.604, 3.106),
}

# Conversion des coordonnées GPS en EPSG:3857 (Web Mercator) en mètres
def gps_to_web_mercator(lat, lon):
    """Convertir GPS (lat, lon) en coordonnées Web Mercator (x, y)"""
    x = lon * 20037508.34 / 180.0
    y = math.log(math.tan((90 + lat) * math.pi / 360.0)) * 20037508.34 / math.pi
    return x, y

# Création d'un dictionnaire avec les coordonnées converties
DELIVERY_SITES = {
    name: gps_to_web_mercator(lat, lon)
    for name, (lat, lon) in DELIVERY_SITES_GPS.items()
}

# Spécifications de livraison : (nombre de livraisons par jour, kg par livraison)
DELIVERY_SPECS = {
    'ONERA': (5, 1.0),
    'CHU_Lille': (5, 0.4),
    'Aerodrome_Marcq': (5, 0.6),
    'Grand_Palais': (5, 0.5),
    'EuraTechnologies': (5, 0.5),
}

# Paramètres du drone
DRONE_PARAMS = {
    'max_payload': 2.0,  # kg
    'max_range': 15000.0,  # m (15 km)
    'base_consumption': 20.0,  # Wh/km
    'load_consumption': 10.0,  # Wh/km par kg supplémentaire
    'base_speed': 25.0,  # km/h
    'speed_reduction': 0.15,  # réduction de 15% par kg
    'battery_capacity': 2600.0,  # Wh (estimation)
}

# Nombre de drones
NUM_DRONES = 5

# Paramètres météorologiques (Jalon 4)
METEO_PARAMS = {
    'T0': 0,      # Temps de départ (secondes)
    'N0': 300,    # Début de la pluie (secondes)
    'N1': 600,    # Fin de la pluie (secondes)
}

# Constantes extraites
CITADELLE = DELIVERY_SITES['Parc_Citadelle']
CONSO_BASE = DRONE_PARAMS['base_consumption']
CONSO_POIDS = DRONE_PARAMS['load_consumption']
VITESSE_BASE = DRONE_PARAMS['base_speed']
PENALITE_V = DRONE_PARAMS['speed_reduction']
MAX_PAYLOAD = DRONE_PARAMS['max_payload']
MAX_RANGE = DRONE_PARAMS['max_range']

# Dictionnaire des cibles de livraison
CIBLES = {}
for site_name, num_livraisons in list(DELIVERY_SPECS.items()):
    CIBLES[site_name] = {
        'pos': DELIVERY_SITES[site_name],
        'masse': num_livraisons[1],  # Masse par livraison
        'reste': num_livraisons[0],  # Nombre de livraisons restantes
    }

# Météo
T0 = METEO_PARAMS['T0']
N0 = METEO_PARAMS['N0']
N1 = METEO_PARAMS['N1']
