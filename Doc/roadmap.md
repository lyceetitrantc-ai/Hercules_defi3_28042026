# Roadmap du Projet : Planification Intégrée pour un Réseau de Drones Urbains

## Vue d'ensemble
Le projet est divisé en 4 jalons principaux, avec un jalon bonus. Vous disposez de 4 heures pour réaliser l'ensemble. La répartition du temps est basée sur les pourcentages donnés (ajustés pour totaliser 100% en incluant le bonus).

- **Temps total estimé** : 4 heures (240 minutes)
- **Répartition** :
  - Jalon 1 : 20% ≈ 48 minutes
  - Jalon 2 : 30% ≈ 72 minutes
  - Jalon 3 : 30% ≈ 72 minutes
  - Jalon 4 (Bonus) : 10% ≈ 24 minutes

## Jalons et Tâches Détaillées

### Jalon 1 : Modélisation CAO des Drones avec Capteurs (48 min)
**Objectif** : Modéliser en 3D les drones avec capteurs pour la navigation urbaine.

**Tâches** :
1. Analyser le système énergétique (batterie, moteurs, contrôleur, etc.) - 10 min
2. Sélectionner des composants commerciaux et concevoir en CAO (géométries simplifiées) - 15 min
3. Calculer le poids total du drone - 5 min
4. Créer l'assemblage CAO de tous les composants - 18 min

**Spécifications** :
- Flotte de 5 unités
- Capacité : 2 kg, Autonomie : 15 km, Consommation : 20 Wh/km + 10 Wh/km/kg, Vitesse : 25 km/h - 15%/kg

### Jalon 2 : Simulation de l’Efficacité Énergétique des Itinéraires (72 min)
**Objectif** : Simuler les itinéraires sur Python/MATLAB pour évaluer énergie et temps.

**Tâches** :
1. Collecter les coordonnées GPS des points de livraison (Parc Citadelle, ONERA, CHU Lille, Aérodrome, Grand Palais, EuraTechnologies) - 15 min
2. Convertir en coordonnées X,Y (EPSG:3857) - 10 min
3. Implémenter la simulation énergétique et temporelle - 30 min
4. Créer un graphique 2D des trajectoires colorées avec évolution temporelle - 17 min

**Spécifications** :
- Livraisons : 2 kg chacun
- Montrer trajectoires en couleurs avec temps

### Jalon 3 : Développement d’un Algorithme de Planification d’Itinéraires (72 min)
**Objectif** : Développer un algorithme optimal pour planifier les trajets.

**Tâches** :
1. Analyser les livraisons multiples (5/jour par site, poids variables) - 10 min
2. Implémenter l'algorithme d'optimisation (consommation énergie + temps total) - 40 min
3. Générer le graphique 2D des trajectoires optimisées - 22 min

**Spécifications** :
- Drones peuvent livrer plusieurs points par trajet
- Poste unique : Parc Citadelle
- Livraisons : ONERA (1kg x5), CHU (0.4kg x5), Aérodrome (0.6kg x5), Grand Palais (0.5kg x5), EuraTechnologies (0.5kg x5)

### Jalon 4 : Ajustement en Temps Réel des Itinéraires (Bonus, 24 min)
**Objectif** : Intégrer les conditions météorologiques (pluies).

**Tâches** :
1. Implémenter la logique de pause pendant la pluie (T0+N0 à T0+N1) - 15 min
2. Mettre à jour le graphique avec points d'arrêt - 9 min

**Spécifications** :
- Exemple : T0=0s, N0=300s, N1=600s
- Drones en pause sur place

## Conseils pour les 4 heures
- Respectez les temps estimés pour couvrir tous les jalons.
- Commencez par les jalons 1 et 2 pour les bases, puis 3 pour l'optimisation.
- Le bonus est optionnel si le temps manque.
- Utilisez des outils comme Fusion 360 pour CAO, Python pour simulations/algorithmes.
- Documentez chaque étape dans les dossiers correspondants.