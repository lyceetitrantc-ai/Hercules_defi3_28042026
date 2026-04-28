import math
import matplotlib
matplotlib.use('Agg')  # Mode non-interactif
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Jalon2_Simulation_Energie.donnees import *
from planning import planifier_optimise, distance, calc_energie, calc_temps
import numpy as np

def afficher_resultat():
    """Exécuter la planification et afficher les résultats"""
    
    # Exécuter l'algorithme de planification
    trajets, temps_base, energie_totale = planifier_optimise()
    
    # Calculer les statistiques
    temps_max = 0
    nb_trajets = 0
    for depart, arrivee, t_arr, drone_id in trajets:
        temps_max = max(temps_max, t_arr)
        nb_trajets += 1
    
    # Affichage console des résultats
    print("="*60)
    print("JALON 3 : PLANIFICATION D'ITINÉRAIRES OPTIMISÉE")
    print("="*60)
    print(f"\nRésumé de la planification :")
    print(f"  Nombre de trajets : {nb_trajets}")
    print(f"  Énergie totale consommée : {energie_totale:.2f} Wh")
    print(f"  Temps total de tous les trajets : {temps_max:.1f} secondes ({temps_max/60:.2f} minutes)")
    print(f"  Nombre de drones utilisés : {NUM_DRONES}")
    
    # Statistiques par drone
    drones_trajets = {}
    for depart, arrivee, t_arr, drone_id in trajets:
        if drone_id not in drones_trajets:
            drones_trajets[drone_id] = {'count': 0, 'temps': 0}
        drones_trajets[drone_id]['count'] += 1
        drones_trajets[drone_id]['temps'] = max(drones_trajets[drone_id]['temps'], t_arr)
    
    print(f"\nDétail par drone :")
    for drone_id in sorted(drones_trajets.keys()):
        info = drones_trajets[drone_id]
        print(f"  Drone {drone_id} : {info['count']} trajets, durée totale {info['temps']:.1f}s")
    
    # Générer la visualisation
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Couleurs pour les drones
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    # Placer la base (Citadelle)
    ax.scatter(CITADELLE[0], CITADELLE[1], c='black', s=400, marker='*', 
               label='Parc Citadelle (Base)', zorder=5, edgecolors='gold', linewidths=2)
    
    # Placer les points de livraison
    for nom, pos in DELIVERY_SITES.items():
        if nom != 'Parc_Citadelle':
            ax.scatter(pos[0], pos[1], s=150, marker='o', alpha=0.7, label=nom, zorder=4)
    
    # Dessiner les trajets
    for depart, arrivee, t_arr, drone_id in trajets:
        color = colors[(drone_id - 1) % len(colors)]
        
        # Tracer la ligne de trajet
        ax.plot([depart[0], arrivee[0]], [depart[1], arrivee[1]], 
                color=color, alpha=0.5, linewidth=2, linestyle='-')
        
        # Ajouter la flèche de direction
        dx = arrivee[0] - depart[0]
        dy = arrivee[1] - depart[1]
        ax.annotate('', xy=arrivee, xytext=(depart[0] + 0.8*dx, depart[1] + 0.8*dy),
                    arrowprops=dict(arrowstyle='->', color=color, alpha=0.6, lw=1.5))
        
        # Ajouter le temps d'arrivée
        ax.text(arrivee[0], arrivee[1] + 100, f'{int(t_arr)}s', 
                fontsize=8, color=color, fontweight='bold', ha='center')
    
    # Ajouter une légende pour les drones
    drone_handles = [mpatches.Patch(color=colors[i % len(colors)], 
                                    label=f'Drone {i+1}') 
                     for i in range(NUM_DRONES)]
    
    ax.legend(handles=list(ax.get_legend_handles_labels()[0]) + drone_handles,
              loc='upper left', fontsize=9, ncol=2)
    
    ax.set_title("Réseau de Livraison - Planification Optimisée (Jalon 3)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("X (m) - Coordonnées Web Mercator", fontsize=11)
    ax.set_ylabel("Y (m) - Coordonnées Web Mercator", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Améliorer la présentation
    plt.tight_layout()
    plt.savefig('planification_optimisee.png', dpi=150, bbox_inches='tight')
    print(f"\n[OK] Graphique sauvegarde : planification_optimisee.png")
    
    plt.close()

def afficher_statistiques_detaillees():
    """Afficher des statistiques détaillées sur la planification"""
    
    trajets, _, energie_totale = planifier_optimise()
    
    print("\n" + "="*60)
    print("STATISTIQUES DÉTAILLÉES")
    print("="*60)
    
    # Vérifier les livraisons
    print("\nLivraisons à effectuer :")
    for site, (nb, masse) in DELIVERY_SPECS.items():
        print(f"  {site:20s} : {nb} livraisons × {masse} kg")
    
    # Consommation d'énergie par site
    print(f"\nÉnergie totale disponible par drone : {DRONE_PARAMS['battery_capacity']:.0f} Wh")
    print(f"Énergie totale consommée : {energie_totale:.2f} Wh")
    print(f"Capacité utilisée : {(energie_totale / (DRONE_PARAMS['battery_capacity'] * NUM_DRONES)) * 100:.1f}%")
    
    # Temps de vol
    print(f"\nNombre total de trajets : {len(trajets)}")
    temps_max = max(t for _, _, t, _ in trajets)
    print(f"Durée maximale (incluant pauses météo) : {temps_max:.1f}s ({temps_max/60:.2f}min)")

if __name__ == "__main__":
    afficher_resultat()
    afficher_statistiques_detaillees()
