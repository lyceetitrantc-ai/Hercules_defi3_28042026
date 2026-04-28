======================================================================
PROJET LILLE - DÉFI 3 : PLANIFICATION D'UN RÉSEAU DE DRONES URBAINS
======================================================================

1. DESCRIPTION DU PROJET
----------------------------------------------------------------------
Ce projet propose une solution algorithmique optimisée pour la gestion 
d'une flotte de drones de livraison dans la ville de Lille. L'objectif 
est de planifier des itinéraires depuis la Citadelle vers 5 cibles 
stratégiques, en minimisant le temps et la consommation d'énergie, 
tout en respectant les contraintes météorologiques.

2. ARCHITECTURE LOGICIELLE (PYTHON)
----------------------------------------------------------------------
Le système repose sur deux fichiers interdépendants :

A. donnees.py (La base de connaissances)
   Ce fichier stocke l'intégralité des variables d'environnement et 
   des coordonnées géographiques au format cartésien (X, Y) en mètres.
   - Constantes cinématiques (Vitesse de base : 25 km/h).
   - Constantes énergétiques (Conso de base : 20 Wh/km).
   - Variables météorologiques (T0=0, N0=300, N1=600).
   - Dictionnaire des 5 cibles avec leurs masses respectives (0.5 ou 0.6 kg)
     et le quota de livraisons (5 par cible).

B. main.py (Le moteur de calcul)
   Ce script exécute la logique de mission selon une approche "gloutonne"
   (Greedy Algorithm). Il contient :
   - Les fonctions de calcul physique (distance, énergie, temps).
   - Le module de vérification météo pour le jalon d'intempéries.
   - La boucle d'exécution qui sélectionne la cible la plus proche, 
     calcule le vol aller (chargé), met à jour les quotas, puis calcule 
     le vol retour (à vide).
   - Le module de rendu visuel (matplotlib) pour générer la carte 2D.

3. LOGIQUE PHYSIQUE ET CONTRAINTES (CAHIER DES CHARGES)
----------------------------------------------------------------------
Le code applique mathématiquement les règles suivantes pour chaque segment :
- DISTANCE : Calculée via la distance euclidienne (théorème de Pythagore).
- VITESSE : Réduction de 15% de la vitesse nominale pour chaque kg embarqué.
- ÉNERGIE : Pénalité de +10 Wh/km pour chaque kg embarqué.
- MÉTÉO (JALON) : Si un drone est en vol entre la seconde 300 et la 
  seconde 600, il se met en "pause" (vol stationnaire). La durée de 
  l'averse subie est ajoutée au temps de vol total sans modifier le trajet.

4. MODE D'EMPLOI
----------------------------------------------------------------------
Prérequis : Disposer de Python 3 et de la bibliothèque matplotlib.

1. Placez "donnees.py" et "main.py" dans le même répertoire.
2. Exécutez le fichier "main.py".
3. La console affichera le temps total de la mission (en secondes) 
   et l'énergie totale consommée (en Wh).
4. Une fenêtre graphique s'ouvrira, présentant :
   - L'emplacement de la Citadelle et des cibles.
   - Les lignes de vol.
   - Le temps chronométré à l'arrivée de chaque livraison, prouvant 
     la prise en compte de la dynamique temporelle et des pauses météo.

======================================================================
Système de Planification Javis - 2026
======================================================================