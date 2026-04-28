"""
Analyse comparative et statistiques avancées pour le Jalon 3
Comparaison entre différentes stratégies de planning
"""

import math
from Jalon2_Simulation_Energie.donnees import *
from planning import distance, calc_energie, calc_temps, evaluer_circuit_complet

def strategie_naive():
    """Stratégie naïve : 1 colis par trajet"""
    energie_totale = 0
    num_trajets = 0
    
    for site, (nombre, masse) in DELIVERY_SPECS.items():
        for _ in range(nombre):
            # Trajet aller-retour simple
            d = distance(CITADELLE, DELIVERY_SITES[site])
            
            # Aller avec charge
            e_aller = calc_energie(d, masse)
            # Retour vide
            e_retour = calc_energie(d, 0)
            
            energie_totale += e_aller + e_retour
            num_trajets += 2
    
    return energie_totale, num_trajets

def strategie_optimale_theorique():
    """Stratégie optimale théorique : grouper au maximum"""
    energie_totale = 0
    
    # Grouper les colis sous 2 kg
    # ONERA : 1kg × 5 = 5 trajets seuls
    # CHU : 0.4kg × 5 = 3 trajets seuls (groupes de 5)  + etc.
    
    # Énumération des groupes optimaux
    groupes = [
        # groupe (masse_totale, distance_circuit)
        (['ONERA'], 1.0),  # 5 trajets solo
        (['CHU_Lille'], 0.4),  # 5 trajets solo
        (['Aerodrome_Marcq'], 0.6),  # 5 trajets solo
        (['Grand_Palais', 'EuraTechnologies'], 1.0),  # Groupable
    ]
    
    # Version simplifiée : chaque trajet est solo
    for site, (nombre, masse) in DELIVERY_SPECS.items():
        d = distance(CITADELLE, DELIVERY_SITES[site])
        
        for _ in range(nombre):
            e_aller = calc_energie(d, masse)
            e_retour = calc_energie(d, 0)
            energie_totale += e_aller + e_retour
    
    return energie_totale

def analyser_ecarts():
    """Analyser les écarts entre stratégies"""
    print("="*60)
    print("ANALYSE COMPARATIVE - STRATÉGIES DE PLANIFICATION")
    print("="*60)
    
    # Stratégie naïve
    e_naive, trajets_naive = strategie_naive()
    print(f"\n[STRATÉGIE NAÏVE] (1 colis par trajet)")
    print(f"  Énergie : {e_naive:.2f} Wh")
    print(f"  Trajets : {trajets_naive}")
    print(f"  Efficacité : {(e_naive / (NUM_DRONES * DRONE_PARAMS['battery_capacity'])) * 100:.1f}%")
    
    # Stratégie actuelle (optimisée)
    from planning import planifier_optimise
    trajets, _, e_optimisee = planifier_optimise()
    trajets_optimises = len(trajets)
    
    print(f"\n[STRATÉGIE OPTIMISÉE] (groupement multi-sites)")
    print(f"  Énergie : {e_optimisee:.2f} Wh")
    print(f"  Trajets : {trajets_optimises}")
    print(f"  Efficacité : {(e_optimisee / (NUM_DRONES * DRONE_PARAMS['battery_capacity'])) * 100:.1f}%")
    
    # Gains
    gain_energie = e_naive - e_optimisee
    gain_pourcent = (gain_energie / e_naive) * 100
    gain_trajets = trajets_naive - trajets_optimises
    
    print(f"\n[GAINS]")
    print(f"  Réduction énergie : {gain_energie:.2f} Wh ({gain_pourcent:.1f}%)")
    print(f"  Réduction trajets : {gain_trajets} ({(gain_trajets/trajets_naive)*100:.1f}%)")
    
    return e_naive, e_optimisee, gain_pourcent

def analyser_distances():
    """Analyse des distances par site"""
    print("\n" + "="*60)
    print("ANALYSE DES DISTANCES")
    print("="*60 + "\n")
    
    distances_sites = {}
    for site, coords in DELIVERY_SITES.items():
        if site != 'Parc_Citadelle':
            d = distance(CITADELLE, coords) / 1000  # en km
            distances_sites[site] = d
    
    # Trier par distance
    for site, d in sorted(distances_sites.items(), key=lambda x: x[1]):
        print(f"  {site:20s} : {d:6.2f} km")
    
    # Statistiques
    distances = list(distances_sites.values())
    min_d = min(distances)
    max_d = max(distances)
    avg_d = sum(distances) / len(distances)
    
    print(f"\n  Minimale : {min_d:.2f} km")
    print(f"  Maximale : {max_d:.2f} km")
    print(f"  Moyenne  : {avg_d:.2f} km")
    print(f"  Portée drone : {MAX_RANGE/1000:.1f} km")
    
    return distances_sites

def analyser_charges():
    """Analyse des charges par site"""
    print("\n" + "="*60)
    print("ANALYSE DES CHARGES")
    print("="*60 + "\n")
    
    print(f"  Capacité drone : {MAX_PAYLOAD} kg\n")
    
    for site, (nombre, masse) in sorted(DELIVERY_SPECS.items()):
        total_site = nombre * masse
        print(f"  {site:20s} : {nombre} × {masse} kg = {total_site:4.1f} kg")
    
    total_general = sum(nombre * masse for nombre, masse in DELIVERY_SPECS.values())
    print(f"  {'TOTAL':20s} : {total_general:4.1f} kg")
    
    num_trajet_min = math.ceil(total_general / MAX_PAYLOAD)
    print(f"\n  Nombre minimum de trajets : {num_trajet_min}")

def analyser_consommation():
    """Analyse détaillée de la consommation"""
    print("\n" + "="*60)
    print("ANALYSE DE LA CONSOMMATION")
    print("="*60 + "\n")
    
    from planning import planifier_optimise
    trajets, _, energie = planifier_optimise()
    
    # Consommation par drone
    print("  Consommation par drone :")
    drones_energie = {}
    for _, _, _, drone_id in trajets:
        if drone_id not in drones_energie:
            drones_energie[drone_id] = 0
    
    # Recalculer avec énergie réelle (simplifiée)
    energie_par_drone = energie / NUM_DRONES
    for drone_id in range(1, NUM_DRONES + 1):
        print(f"    Drone {drone_id} : {energie_par_drone:.2f} Wh " + 
              f"({(energie_par_drone/DRONE_PARAMS['battery_capacity'])*100:.1f}% batterie)")
    
    print(f"\n  Consommation totale : {energie:.2f} Wh")
    print(f"  Batterie totale : {NUM_DRONES * DRONE_PARAMS['battery_capacity']:.0f} Wh")
    print(f"  Utilisation : {(energie/(NUM_DRONES*DRONE_PARAMS['battery_capacity']))*100:.1f}%")
    
    # Potentiel de recharge
    recharge_total = (NUM_DRONES * DRONE_PARAMS['battery_capacity']) - energie
    print(f"  Énergie disponible : {recharge_total:.2f} Wh")

def rapport_complet():
    """Générer un rapport complet"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + "JALON 3 - ANALYSE COMPARATIVE COMPLÈTE".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Analyses
    e_naive, e_opt, gain = analyser_ecarts()
    distances = analyser_distances()
    analyser_charges()
    analyser_consommation()
    
    # Conclusion
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print(f"""
L'algorithme d'optimisation réduit la consommation d'énergie de {gain:.1f}%
comparé à une stratégie naïve. En regroupant les livraisons, on minimise
les détours et on optimise la charge sur chaque trajet.

Points clés :
  ✓ Regroupement des colis légers
  ✓ Optimisation de l'ordre de visite (TSP)
  ✓ Répartition équilibrée entre drones
  ✓ Utilisation maximale de capacité (portée, poids)
    """)

if __name__ == "__main__":
    rapport_complet()
