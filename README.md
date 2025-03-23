# **Wrecked Ocean**

### __Installation et informations importantes__

## Installation
Pour installer **Wrecked Ocean**, il existe deux méthodes:

- Cloner depuis GitHub:
Pour ce faire, il vous sufit d'éxécuter la commande suivante:
-`git clone https://github.com/Meety004/BATOS-ET-MATS-J.git `

Ensuite, télécharger les librairies nécessaires au fonctionnement du programme grâce à la commande suivante:
-`pip install -r BATOS-ET-MATS-J/requirements.txt `

Pour lancer le programme, naviguez jusqu'au dossier de jeu:
-`cd BATOS-ET-MATS-J `

Enfin, éxécuter la commande suivante:
-`python sources/main.py `

Attention, pour éxécuter ce projet, il vous faudra avoir installé Python auparavant.
Il est conseillé d'utiliser une version comprise entre Python 3.8 et Python 3.12.
Les librairies utilisées ne sont pas complètement compatibles avec Python 3.13.
Les versions antérieures à Python 3.8 n'ont pas été testées et peuvent ne pas supporter le programme.
Pour vérifier votre version de Python, éxécuter la commande:
-`python --version` 

Si Python n'est pas installé, veuillez le télécharger ici: [python.org](https://www.python.org/downloads/) en l'ajoutant au PATH lors de l'installation.

### Fonctionnalités

## __Atention, ce projet en est cours de développment. Toutes les fonctionnalités listées ne sont pas encore implémentées.__

## __**Introduction**__
Le jeu **Wrecked Ocean** est un jeu qui se joue en solo. Vous y incarnerez un pirate cherchant à devenir le meilleur et le plus riche de tous. Pour cela, vous devrez chercher de l'équipement puissant sur des îles et affronterez des ennemis puissants lors de vagues intenses pour récupérer leurs équipements légendaires !
**Wrecked Ocean** est un jeu de réactivité, de stratégie et d'action. Vous pouvez collecter près de 30 équipements différents ainsi que de nombreuses bénédictions.

## __**Les îles**__
Vous pourrez découvrir différentes îles remplies d'équipement qui apparaîtront. Il existe quatre sortes d'îles différentes. Les îles **communes**, les îles **rares**, les îles **mythiques** ainsi que les îles **légendaires**. Chacune de ces îles a une probabilité d'apparition différente.
- Ile Commune: 50%
- Ile Rare: 36%
- Ile Mythique: 10%
- Ile Légendaire: 4%

En vous approchant de ces îles vous aurez différentes issues possibles:
- L'île contient de l'équipement commun, rare, mythique ou légendaire -> une interface d'équipement s'ouvre.
- L'île contient de l'équipement 'malus' -> aucune interface ne s'ouvre et l'île disparait.
- L'île contient une bénédiction -> une interface de bénédictions s'ouvre.

## __**L'équipement**__
Il existe trois types d'équipements différents:
- Les canons
- Les voiles
- Les coques
Lorsque l'interface d'équipement s'ouvrira au moment où vous serez à proximité d'une île, vous pourrez apercevoir dans une première ligne votre équipement actuel du type correspondant à celui se trouvant sur l'île (canons, coque, voile) ainsi que sa rareté et une description des effets. Vous pourrez aussi trouver dans la deuxième ligne la rareté et le type de l'équipement de l'île sur laquelle vous vous trouvez ainsi qu'une description des effets.
Si vous souhaitez équiper l'objet, cliquez sur la touche 'A', qui fermera la fenêtre et vous équipera de l'objet. Au contraire, si vous ne souhaitez pas prendre l'objet, continuez votre chemin. L'équipement s'y trouvant pourra être récupéré par un ennemi, ou disparaitra au bout d'un certain temps.

## __**Les bénédictions**__
Lorsque l'interface des bénédictions s'ouvrira quand vous serez à proximité d'une île, vous pourrez apercevoir l'icône symbolisant la bénédiction se trouvant sur l'île ainsi qu'une description de ses effets. Vous pourrez aussi trouver deux bulles numérotées '1' et '2'. Ces bulles sont vos espaces de stockages de bénédictions. '1' étant l'espace de stockage de votre bénédiction principale, et '2' l'espace de stockage de votre bénédiction secondaire. Si vous souhaitez prendre la bénédiction se trouvant sur l'île, appuyer sur la touche du clavier (1 ou 2) à laquelle vous voulez assigner le déclenchement de la bénédiction. Notez qu'une bénédiction sur l'emplacement principal n'aura pas les mêmes effets que si elle est placée dans l'emplacement secondaire. SI au contraire, elle ne vous intéresse pas, continuez votre chemin. La bénédiction pourra être récupérée par un ennemi, ou disparaitra au bout d'un certain temps.
Vous pouvez avoir jusqu'à deux bénédictions en même temps, une principale et une secondaire.
Pour utiliser les bénédictions, utilisez simplement la touche que vous avez assignée à la bénédiction.
Entre chaque utilisation de bénédiction, il y a un cooldown plus ou moins long selon la bénédiction durant lequel vous ne pourrez pas l'utiliser.

## __**Les ennemis**__
Vous rencontrerez des ennemis durant votre partie. Ces ennemis sont comme vous: ils s'équipent et essayent de régner sur la mer. C'est pourquoi ils vous attaqueront. Au fur et à mesure de la partie, les ennemis que vont rencontrerez seront plus forts, pourrotn utiliser plus de bénédiction et auront un meilleur équipement. Les bateaux ennemis ne s'attaqueront pas entre eux. Leur objectif est de contrer le joueur.

## __**Les boss**__ (Fonctionnalité en développement)
Vous pourrez rencontrer, de temps à autre un boss. Ces boss sont les ennemis les plus forts du jeu. Chacun d'eux à une pièce d'équipement particulière, avec des capacités et des pouvoirs incroyables. En vainquant un boss, vous pourrez récupérer son équipement.
Voici la liste des différents boss présents dans le jeu.
- Le Queen Anne’s Revenge - Capacité: 50% de vitesse supplémentaire (Voile)
- The Flying Dutschman - Capacité: Peut aller temporairement sous l'eau, évitant ainsi les tirs ennemis (Coque)
- Le Fancy - Capacité: 8 Canons (Canon)
Il est possible d'avoir qu'un seul équipement de boss dans son inventaire, choisissez bien.

## __**Contrôles**__
Voici les touches de contrôle de jeu:
- Avancer: `Flèche Haut`
- Gauche: `Flèche Gauche`
- Droite: `Flèche Droite`
- Tirer: `Espace`
- Equiper: `A`
- Pause: `Echap`
- Quitter le jeu: `Tab`
- Choisir bénédicition 1: `1`
- Choisir bénédicition 2: `2`

### Attention, lorsque vous avez la Coque Trouée (équipement malus), vos touches de déplacement seront inversées et deviendront les suivantes:
- Avancer: `Flèche Bas`
- Gauche: `Flèche Droite`
- Droite: `Flèche Gauche`

## __**Liste des équipement**__
**Wrecked Ocean** compte au total **29 pièces d'équipements**. 
Voici la liste de tous ces équiements triés par rareté, avec leur probabilités respectives ainsi que leurs effets.

- Equipement de base, obtensible seulement à l'apparition du joueur.
    - Coque de base
    - Canon de base
    - Voile de base

- Commun
    - Coques:
        - Coque chêne (20%) - Augmente la vitesse maximale de 5%
        - Coque épicéa (10%) - Ajoute 10 à la santé maximale du joueur
        - Coque Trouée (6,66%) - Malus - Inverse les commandes de déplacement
    - Canons:
        - +1 Canon (10%) - Ajoute un canon à l'avant
        - Canon en bronze (20%) - Ajoute 20% de dégâts aux projectiles
        - Canons Rouillés (6,66%) - Malus - Rend les projectiles 15% plus lents
    - Voiles:
        - Voile en toile de jute (20%) - Augmente la vitesse maximale de 5%
        - Voile Trouée (6,66%) - Malus - Diminue la vitesse maximale du joueur de 20%

- Rare
    - Coques:
        - Coque en bouleau (10%) - Ajoute 10 à la santé maximale du joueur et augmente la vitesse maximale de 5%
        - Coque en chêne massif (10%) - Ajoute 75 à la santé maximale du joueur
    - Canons:
        - +2 Canons (10%) - Ajoute un canon à l'avant et à l'arrière
        - Canon en argent (17,5%) - Ajoute 33% de dégats  et 5% de vitesse aux projectiles
        - Canon Ballistique (10%) - Multiplie la distance maximale des projectiles par 2
    - Voiles:
        - Voile Latine (17,5%) - Augmente la vitesse maximale de 10%

- Mythique
    - Coques:
        - Coque en bois magique (12%) - Ajoute 50 à la santé maximale du joueur  et augmente la vitesse maximale de 20% et à une chance de 20% de ne pas se prendre les dégâts
    - Canons:
        - +3 Canons (12%) - Ajoute un canon à l'avant, à l'arrière et dans la diagonale avant droite du bateau
        - Canon en or (12%) - Ajoute 66% de dégats et 10% de vitesse au projectiles et augmente la cadence de tir de 10%
        - Canon à tirs doubles (12%) - Tire un deuxième projectile après chaque tir
    - Voiles:
        - Voile enchantée (12%) - Augmente le vitesse maximale de 25% et augmente la maniabilité de 2%

- Légendaire
    - Coques:
        - Coque légendaire (12,5%) - Ajoute 60 à la santé maximale du joueur  et augmente la vitesse maximale de 30%
    - Canons:
        - +4 Canons (12,5%) - Ajoute un canon à l'avant, à l'arrière et dans les deux diagonales à l'avant du bateau
        - Canon légendaire (12,5%) - Ajoute 133% de dégats et 15% de vitesse au projectiles et augmente la cadence de tir de 10%
    - Voiles:
        - Voile légendaire (12,5%) - Augmente le vitesse maximale de 30% et augmente la maniabilité de 5%

        
## __**Liste des bénédictions**__
**Wrecked Ocean** compte au total **8 bénédictions**. 
Voici la liste de tous ces bénédicitons triées par rareté, avec leur probabilités respectives ainsi que leurs effets.

- Rare
    - __Bénédiction Dash__ (12,5%) (Cooldown - 15 sec)
    -                                             - Emplacement Principal - Permet au joueur de se propulser vers l'avant de manière considérable
                                                  - Emplacement Secondaire - Permet au joueur de se propulser vers l'avant de manière plutôt efficace
      
    - Bénédiction Santé (12,5%) (Cooldown - 40 sec) - Emplacement Principal - Permet au joueur de restaurer 50% de ses points de vie max
                                                   - Emplacement Secondaire - Permet au joueur de restaurer 25% de ses points de vie max
- Mythique
    - Bénédiction d'Aura (20%) (Cooldown - 30sec) - Emplacement Principal - Crée une zone autour du joueur qui infligera entre 2 et 10 dégats aux ennemis en fonction de leur proximité
                                                - Emplacement Secondaire - Crée une zone autour du joueur qui infligera entre 1 et 5 dégats aux ennemis en fonction de leur proximité
    
    - Bénédiction de Rage (20%) (Cooldown - 30sec) - Emplacement Principal - Augmente les dégats et la vitesse du joueur (+50%) pendant 10 sec, mais le limite temporairement à 30 pts de vie
                                                 - Emplacement Secondaire - Augmente les dégats et la vitesse du joueur (+50%) pendant 5 sec, mais le limite temporairement à 20 pts de vie
- Légendaire
    - Bénédiction Godmode (25%) (Cooldown - 40sec) - Emplacement Principal - Permet au joueur de ne pas prendre de dégats pendant 10 sec
                                                 - Emplacement Secondaire - Permet au joueur de ne pas prendre de dégats pendant 5 sec
      
    - Bénédiction Projectile (25%) (Cooldown - 50sec) - Emplacement Principal - Permet au joueur d'envoyer une horde de projectile autour de lui quand il tire pendant 10 sec (tir double)
                                                      - Emplacement Secondaire - Permet au joueur d'envoyer une horde de projectile autour de lui quand il tire pendant 10 sec (tir simple)

## __**Compatibilité**__
**Wrecked Ocean** est compatible sur *Windows 10* et *Windows 11*. Le jeu n'a pas été testé sur les versions antérieures à Windows 10.
Le jeu est aussi compaptible avec Linux. Des tests on été réalisés sur *Ubuntu 24.04.2* ainsi que sur *Debian 12.10.0*.
Le jeu peut fonctionner sur des versions antérieures de ces systèmes d'exploitations, mais cela n'est pas garanti.
Attention, si vous utilisez une machine virtuelle (VM), il se peut que des problèmes liés à la taille de la fenêtre de la machine virtuelle apparaissent.
Faites attention de bien régler vos configurations de VM pour afficher la totalité de l'écran de jeu.


## __**Crédits**__
**Wrecked Ocean** est un jeu réalisé à l'occasion du concours Trophée NSI, dans la catégorie Terminale.
Notre professeur, M. MARIE-JEANNE nous a accompagné pendant toute la durée de ce projet, nous apportant solutions et idées nouvelles.
Voici la liste des élèves ayant participé au projet **Wrecked Ocean**.
- BELLEC-ESCALERA Elliot - Réalisation, Développement
- CADEAU--FLAUJAT Gabriel - Textures, Réalisation, Développement, Documentation
- KELEMEN Thomas - Développement
- GABRIEL Tom - Réalisation vidéo, Textures, Documentation
