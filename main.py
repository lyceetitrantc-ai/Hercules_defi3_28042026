import math
import matplotlib.pyplot as plt
from donnees import *

def distance(p1, p2):
    # Application du théorème de Pythagore pour trouver la ligne droite
    # On soustrait les X et les Y, on les met au carré, et on prend la racine
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def calc_energie(dist, masse):
    # L'énergie totale est l'énergie de base PLUS la pénalité de poids
    # On multiplie la pénalité par la masse embarquée, on ajoute à la base, puis on multiplie par les mètres
    return (CONSO_BASE + (PENALITE_E * masse)) * dist

def calc_temps(dist, masse):
    # Le poids freine le drone. On calcule le pourcentage de vitesse restante (ex: 1 - 0.15 * 0.6 = 91%)
    vitesse = VITESSE_BASE * (1 - (PENALITE_V * masse))
    # Le temps en secondes est simplement la distance divisée par cette vitesse réelle
    return dist / vitesse

def verif_meteo(t_deb, t_fin):
    # On vérifie si l'heure de vol (t_deb à t_fin) croise l'heure de la pluie (N0 à N1)
    if t_deb < N1 and t_fin > N0:
        # Si oui, on calcule la durée exacte passée sous la pluie pour mettre le drone en pause
        return min(t_fin, N1) - max(t_deb, N0)
    # Si le vol est en dehors des heures de pluie, aucune pause (0 seconde)
    return 0

def executer_planification():
    # Initialisation du chronomètre, du compteur électrique et de la boîte noire (historique)
    t_global = T0
    e_totale = 0
    trajets = []

    # Tant qu'il reste au moins 1 colis à livrer n'importe où
    while any(c["reste"] > 0 for c in CIBLES.values()):
        cible_proche = None
        d_min = float('inf')

        # On scanne toutes les cibles pour trouver la plus proche qui a encore besoin de colis
        for nom, data in CIBLES.items():
            if data["reste"] > 0:
                d = distance(CITADELLE, data["pos"])
                if d < d_min:
                    d_min = d
                    cible_proche = nom

        cible = CIBLES[cible_proche]

        # --- PHASE 1 : LE VOL ALLER (Chargé) ---
        # Calcul du temps avec le poids du colis
        t_aller = calc_temps(d_min, cible["masse"])
        # On vérifie si on s'est pris la pluie sur le chemin
        pause_aller = verif_meteo(t_global, t_global + t_aller)
        # On avance le chronomètre global
        t_global += t_aller + pause_aller
        # On calcule l'énergie consommée avec le poids
        e_aller = calc_energie(d_min, cible["masse"])

        # On valide la livraison et on l'enregistre dans l'historique
        cible["reste"] -= 1
        trajets.append((CITADELLE, cible["pos"], t_global))

        # --- PHASE 2 : LE VOL RETOUR (À vide) ---
        # Même logique, mais la masse est de 0 kg
        t_retour = calc_temps(d_min, 0)
        pause_retour = verif_meteo(t_global, t_global + t_retour)
        t_global += t_retour + pause_retour
        e_retour = calc_energie(d_min, 0)

        # On enregistre le retour à la Citadelle et on cumule l'énergie
        trajets.append((cible["pos"], CITADELLE, t_global))
        e_totale += e_aller + e_retour

    return trajets, t_global, e_totale

def afficher_carte(trajets):
    # On prépare une toile blanche de bonne taille
    plt.figure(figsize=(10, 8))
    
    # On place l'étoile de la Citadelle
    plt.scatter(CITADELLE[0], CITADELLE[1], c='red', s=200, marker='*', label='Citadelle (Recharge)')
    
    # On place les points des cibles
    for nom, data in CIBLES.items():
        plt.scatter(data["pos"][0], data["pos"][1], s=100, label=nom)
        
    # On dessine chaque vol depuis notre historique
    for depart, arrivee, t_arr in trajets:
        # Trace la ligne semi-transparente
        plt.plot([depart[0], arrivee[0]], [depart[1], arrivee[1]], 'k-', alpha=0.4)
        # Écrit l'heure d'arrivée sur la carte
        plt.text(arrivee[0], arrivee[1], f" {int(t_arr)}s", fontsize=8, color='blue')

    # Titres et légendes pour faire propre
    plt.title("Réseau de Livraison - Planification Optimisée")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.legend()
    plt.grid(True)
    plt.show()