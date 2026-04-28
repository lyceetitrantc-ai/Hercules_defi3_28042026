import math
from donnees import *
from itertools import combinations, permutations

def distance(p1, p2):
    """Calculer la distance entre deux points (Théorème de Pythagore)"""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def calc_energie(dist_en_m, masse):
    """Calculer l'énergie consommée pour une distance donnée avec une charge"""
    dist_en_km = dist_en_m / 1000.0
    return (CONSO_BASE + (CONSO_POIDS * masse)) * dist_en_km

def calc_temps(dist_en_m, masse):
    """Calculer le temps de vol pour une distance donnée avec une charge"""
    dist_en_km = dist_en_m / 1000.0
    # Le poids freine le drone
    vitesse = VITESSE_BASE * (1 - (PENALITE_V * masse)) if masse < (1.0 / PENALITE_V) else 1.0
    if vitesse <= 0:
        return float('inf')
    return dist_en_km / vitesse * 3600  # Retourner en secondes

def verif_meteo(t_deb, t_fin):
    """Vérifier si un vol croise une période de pluie et retourner le temps de pause"""
    if t_deb < N1 and t_fin > N0:
        return min(t_fin, N1) - max(t_deb, N0)
    return 0

def distance_circuit(sites_coords):
    """Calculer la distance totale d'un circuit partant et revenant à la Citadelle"""
    total = distance(CITADELLE, sites_coords[0])
    for i in range(len(sites_coords) - 1):
        total += distance(sites_coords[i], sites_coords[i + 1])
    total += distance(sites_coords[-1], CITADELLE)
    return total

def evaluer_circuit_complet(sites_coords, masses):
    """Évaluer la consommation d'énergie para un circuit complet"""
    if not sites_coords:
        return 0, 0
    
    energie_totale = 0
    temps_total = 0
    
    points = [CITADELLE] + sites_coords
    masse_actuelle = sum(masses)
    
    for i in range(len(points) - 1):
        dist = distance(points[i], points[i + 1])
        e = calc_energie(dist, masse_actuelle)
        t = calc_temps(dist, masse_actuelle)
        
        pause = verif_meteo(temps_total, temps_total + t)
        temps_total += t + pause
        energie_totale += e
        
        # Réduire la masse pour le segment suivant
        if i < len(masses):
            masse_actuelle -= masses[i]
    
    # Retour à la base
    dist_retour = distance(sites_coords[-1], CITADELLE)
    e_retour = calc_energie(dist_retour, 0)
    t_retour = calc_temps(dist_retour, 0)
    pause_retour = verif_meteo(temps_total, temps_total + t_retour)
    temps_total += t_retour + pause_retour
    energie_totale += e_retour
    
    return energie_totale, temps_total

def construire_circuit_optimal(sites, masses):
    """Construire le meilleur circuit pour une liste de sites donnés (TSP simple)"""
    if len(sites) == 1:
        return sites, masses
    
    # Pour un petit nombre de sites, tester toutes les permutations
    if len(sites) <= 6:
        meilleur_permut = sites
        meilleur_energie = float('inf')
        
        for perm in permutations(range(len(sites))):
            sites_permutes = [sites[i] for i in perm]
            masses_permutes = [masses[i] for i in perm]
            dist = distance_circuit(sites_permutes)
            if dist < distance_circuit(meilleur_permut):
                meilleur_permut = sites_permutes
                meilleur_energie = dist
        
        return meilleur_permut, [masses[sites.index(s)] for s in meilleur_permut]
    else:
        # Heuristique nearest neighbor pour plus de sites
        non_visites = list(range(len(sites)))
        circuit = [0]
        non_visites.remove(0)
        
        while non_visites:
            derniers = circuit[-1]
            plus_proche = min(non_visites, key=lambda j: distance(sites[derniers], sites[j]))
            circuit.append(plus_proche)
            non_visites.remove(plus_proche)
        
        sites_ordonnees = [sites[i] for i in circuit]
        masses_ordonnees = [masses[i] for i in circuit]
        return sites_ordonnees, masses_ordonnees

def planifier_optimise():
    """
    Algorithme d'optimisation pour planifier les trajets multi-livraisons
    Objectif : minimiser l'énergie totale avec contrainte de temps et de poids
    """
    trajets = []
    energie_totale = 0
    
    livraisons_restantes = {
        site: DELIVERY_SPECS[site][0]
        for site in DELIVERY_SPECS
    }
    
    itineraires_drones = [[] for _ in range(NUM_DRONES)]
    drone_idx = 0
    
    while any(v > 0 for v in livraisons_restantes.values()):
        # Chercher la meilleure combinaison pour ce drone
        meilleur_plan = None
        meilleur_energie = float('inf')
        meilleur_masses = None
        
        sites_dispo = [s for s, count in livraisons_restantes.items() if count > 0]
        
        # Essayer différentes combinaisons
        for r in range(1, min(len(sites_dispo) + 1, 4)):  # Max 3 sites par trajet
            for combo in combinations(sites_dispo, r):
                # On peut prendre 1 à N livraisons à chaque site
                # Pour simplifier, on prend 1 livraison à la fois
                masse_total = sum(DELIVERY_SPECS[s][1] for s in combo)
                
                if masse_total > MAX_PAYLOAD:
                    continue
                
                # Vérifier la portée
                sites_coords = [DELIVERY_SITES[s] for s in combo]
                dist_totale = distance_circuit(sites_coords)
                
                if dist_totale > MAX_RANGE:
                    continue
                
                # Construire le circuit optimal
                sites_ordonnes, masses = construire_circuit_optimal(
                    sites_coords, 
                    [DELIVERY_SPECS[s][1] for s in combo]
                )
                
                e, t = evaluer_circuit_complet(sites_ordonnes, masses)
                
                if e < meilleur_energie:
                    meilleur_energie = e
                    meilleur_plan = list(zip(combo, [DELIVERY_SITES[s] for s in combo]))
                    meilleur_masses = [DELIVERY_SPECS[s][1] for s in combo]
        
        # Si pas de plan trouvé, prendre le site le plus proche
        if meilleur_plan is None:
            dist_min = float('inf')
            site_proche = None
            for site in sites_dispo:
                d = distance(CITADELLE, DELIVERY_SITES[site])
                if d < dist_min:
                    dist_min = d
                    site_proche = site
            
            meilleur_plan = [(site_proche, DELIVERY_SITES[site_proche])]
            meilleur_masses = [DELIVERY_SPECS[site_proche][1]]
        
        # Enregistrer le plan pour ce drone
        itineraires_drones[drone_idx] = meilleur_plan
        
        # Mettre à jour les livraisons restantes
        for site_name, _ in meilleur_plan:
            livraisons_restantes[site_name] -= 1
        
        drone_idx = (drone_idx + 1) % NUM_DRONES
    
    # Exécuter tous les trajets et créer la visualisation
    for drone_id, plan in enumerate(itineraires_drones):
        if not plan:
            continue
        
        temps_drone = T0
        
        # Extraire les coordonnées
        coords = [p[1] for p in plan]
        masses = [DELIVERY_SPECS[p[0]][1] for p in plan]
        
        # Construire et évaluer le circuit
        coords_ordonnes, masses_finales = construire_circuit_optimal(coords, masses)
        
        # Simuler le circuit
        points = [CITADELLE] + coords_ordonnes
        
        for i in range(len(points) - 1):
            dist = distance(points[i], points[i + 1])
            masse_actuelle = sum(masses_finales[i:]) if i < len(masses_finales) else 0
            
            t = calc_temps(dist, masse_actuelle)
            e = calc_energie(dist, masse_actuelle)
            
            pause = verif_meteo(temps_drone, temps_drone + t)
            temps_drone += t + pause
            energie_totale += e
            
            trajets.append((points[i], points[i + 1], temps_drone, drone_id + 1))
        
        # Retour à la base
        dist_retour = distance(coords_ordonnes[-1], CITADELLE)
        t_retour = calc_temps(dist_retour, 0)
        e_retour = calc_energie(dist_retour, 0)
        
        pause_retour = verif_meteo(temps_drone, temps_drone + t_retour)
        temps_drone += t_retour + pause_retour
        energie_totale += e_retour
        
        trajets.append((coords_ordonnes[-1], CITADELLE, temps_drone, drone_id + 1))
    
    return trajets, T0, energie_totale
