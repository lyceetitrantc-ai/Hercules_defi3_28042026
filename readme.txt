======================================================================
PROJET LILLE - DÉFI 3 : SIMULATION DYNAMIQUE ET CONTRÔLE DU DRONE
======================================================================

1. OBJECTIF DE LA SIMULATION
----------------------------------------------------------------------
Cette simulation a pour but de valider le comportement en vol du drone 
quadricoptère modélisé pour la ville de Lille. Elle prouve mathématiquement 
que le système de contrôle embarqué est capable de stabiliser l'appareil 
(vol stationnaire, compensation du vent, déplacement) malgré les variations 
de charge utile (colis de 0.5 kg ou 0.6 kg).

2. RÔLE DES FICHIERS
----------------------------------------------------------------------
A. init_param.m (Le dictionnaire physique)
   C'est le script d'initialisation. Il charge dans la mémoire locale toutes 
   les constantes réelles de notre drone avant le vol :
   - Masse à vide (m = 0.468 kg) et Gravité.
   - Matrices d'inertie (Ixx, Iyy, Izz) qui définissent comment le drone 
     résiste aux rotations.
   - Constantes aérodynamiques des hélices (portance 'k' et traînée 'b').
   - Coefficients de frottement de l'air (Ax, Ay, Az).

B. mon_drone.slx (Le moteur de simulation)
   C'est le schéma-blocs Simulink. Il représente le "cerveau" du drone 
   connecté aux lois de la physique.

3. ARCHITECTURE LOGIQUE (Comment ça fonctionne)
----------------------------------------------------------------------
Le modèle Simulink fonctionne en boucle fermée selon 4 étapes majeures :

Étape 1 : La Consigne (Ce qu'on veut)
Le système reçoit un ordre de vol (ex: "Monter à 10 mètres" ou "Avancer").

Étape 2 : Le Contrôleur PD (Le pilote automatique)
Le système compare la position réelle du drone avec la consigne. 
S'il y a un écart (erreur), le contrôleur Proportionnel-Dérivé calcule 
la force de correction nécessaire sur les 4 axes :
- Thrust (Poussée globale vers le haut)
- Roll (Roulis / inclinaison gauche-droite)
- Pitch (Tangage / inclinaison avant-arrière)
- Yaw (Lacet / rotation sur lui-même)

Étape 3 : Le fcn_mixer (Le répartiteur)
Ce bloc mathématique traduit les 4 commandes de vol (Thrust, Roll, Pitch, Yaw) 
en vitesses de rotation spécifiques (en rad/s) pour chacun des 4 moteurs 
indépendants. 

Étape 4 : Le fcn_dynamics (La réalité physique)
C'est ici que les équations d'Euler s'appliquent. Ce bloc prend la vitesse 
des 4 moteurs, applique la gravité, l'inertie et les frottements d'air 
définis dans "init_param.m", et calcule la nouvelle position (X, Y, Z) 
et la nouvelle inclinaison du drone à l'instant T+1. 
Cette nouvelle position est renvoyée au contrôleur (Retour à l'Étape 2).

4. INSTRUCTIONS D'EXÉCUTION (Marche à suivre)
----------------------------------------------------------------------
Pour lancer une simulation propre :
1. Ouvrir MATLAB.
2. Exécuter d'abord le script "init_param.m" dans le Command Window. 
   (Vérifiez que le Workspace se remplit avec les variables).
3. Ouvrir le modèle "mon_drone.slx".
4. Lancer la simulation (bouton Run).
5. Ouvrir les blocs "Scope" (oscilloscopes) pour observer les courbes 
   qui démontrent la stabilisation de l'altitude et des angles en 
   quelques fractions de seconde.

5. LIEN AVEC LA MISSION (Python)
----------------------------------------------------------------------
Pendant que l'algorithme de routage calcule l'itinéraire global sur la 
carte de Lille, cette simulation garantit que chaque mètre parcouru est 
réalisé de manière stable et sécurisée pour les colis transportés.
======================================================================