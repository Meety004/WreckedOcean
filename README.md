# **Wrecked Ocean**

# __**Installation et informations importantes**__

## __**Installation**__
Pour installer **Wrecked Ocean**, il existe deux méthodes:

### Cloner depuis GitHub:
Pour ce faire, il vous sufit d'éxécuter la commande suivante dans un terminal:
- ```git clone https://github.com/Meety004/WreckedOcean.git ```

Ensuite, téléchargez les librairies nécessaires au fonctionnement du programme grâce à la commande suivante:
- ```pip install -r WreckedOcean/requirements.txt ```

Pour lancer le programme, naviguez jusqu'au dossier de jeu:
- ```cd WreckedOcean ```

Enfin, éxécutez la commande suivante:
- ```python sources/main.py ```

Un écran noir s'affichera pendant quelques secondes ou moins, dépendant de votre ordinateur avant de faire apparaitre le menu du jeu.

Attention, pour éxécuter ce projet, il vous faudra avoir installé Python auparavant.

Il est conseillé d'utiliser une version comprise entre Python 3.8 et Python 3.12.9.

Les librairies utilisées ne sont pas complètement compatibles avec Python 3.13.

Les versions antérieures à Python 3.8 n'ont pas été testées et peuvent ne pas supporter le programme.

Pour vérifier votre version de Python, éxécutez la commande:
- ```python --version```

Si Python n'est pas installé, veuillez le télécharger ici: [python.org](https://www.python.org/downloads/) en l'ajoutant au PATH lors de l'installation.

Si vous ne souhaitez pas polluer votre machine avec des librairies, vous pouvez installer et éxécuter le programme dans un environnement virtuel (venv).
Voici la démarche à suivre:
- ```python -m venv /WreckedOceanVenv```
- ```cd WreckedOceanVenv```

Il vous faudra ensuite suivre les étapes listées ci-dessus.
Notez que *WreckedOceanVenv* est une suggestion de nom d'environnement virtuel, il vous est possible de le nommer comme vous le souhaitez.

### Télécharger le fichier zip
Vous pouvez aussi télécharger le fichier zip du projet.
Il vous faudra ensuite extraire les fichiers.

Ensuite, dans un terminal, éxécutez les commandes suivantes une fois que vous êtes dans le répertoire où se situe le jeu.

- ```pip install -r WreckedOcean/requirements.txt ```
- ```cd WreckedOcean ```
- ```python sources/main.py ```

Un écran noir s'affichera pendant quelques secondes ou moins, dépendant de votre ordinateur avant de faire apparaitre le menu du jeu.

Assurez vous d'avoir Python installé pour éxécuter le programme.
Suivez les étapes ci-dessus pour installer Python ou créer un environnement virtuel.

## __**Compatibilité**__
**Wrecked Ocean** est compatible sur *Windows 10* et *Windows 11*. Le jeu n'a pas été testé sur les versions antérieures à Windows 10.

Le jeu est aussi compaptible avec Linux. Des tests on été réalisés sur *Ubuntu 24.04.2* ainsi que sur *Debian 12.10.0*.

Le jeu peut fonctionner sur des versions antérieures de ces systèmes d'exploitations, mais cela n'est pas garanti.

Attention, si vous utilisez une machine virtuelle (VM), il se peut que des problèmes liés à la taille de la fenêtre de la machine virtuelle apparaissent.

Faites attention de bien régler vos configurations de VM pour afficher la totalité de l'écran de jeu.

## __**Problèmes et résolutions**__
**Wrecked Ocean** peut comporter des bugs.
Si vous en rencontrez, vous pouvez contacter *gabriel.flaujat@gmail.com* et *bellecelliot@gmail.com*.

Vous pouvez aussi créer une __*Pull Request*__ sur *GitHub* afin de voir vos modifications ajoutées au projet.

Le jeu est encore en développement, les bugs seront donc corrigés avec les futures mises à jour.



# __**Fonctionnalités**__

## __Atention, ce projet en est cours de développment. Toutes les fonctionnalités listées ne sont pas encore implémentées.__

## __**Introduction**__
Le jeu **Wrecked Ocean** est un jeu qui se joue en solo. Vous y incarnerez un pirate cherchant à devenir le meilleur et le plus riche de tous. Pour cela, vous devrez chercher de l'équipement puissant sur des îles et affronterez des ennemis puissants lors de vagues intenses pour récupérer leurs équipements légendaires !
**Wrecked Ocean** est un jeu de réactivité, de stratégie et d'action. Vous pouvez collecter près de 25 équipements différents ainsi que de nombreuses bénédictions.

Le bateau du joueur:

![Le bateau du joueur](/data/images/README/bateauJoueur.png)

## __**Les îles**__
Vous pourrez voir apparaitre différentes îles remplies d'équipements. Il existe quatre sortes d'îles qui ont des probabilités d'apparition différentes:
-  **Les îles communes**

    ![Les îles communes](/data/images/README/ile_commune.png)

-  **Les îles rares**

    ![Les îles rares](/data/images/README/ile_rare.png)

- **Les îles mythiques**

    ![Les îles mythiques](/data/images/README/ile_mythique.png)

- **Les îles légendaires**

    ![Les îles légendaires](/data/images/README/ile_legendaire.png)

Lors de la première vague, les probabilités sont les suivantes:
- Ile Commune: 56%
- Ile Rare: 41%
- Ile Mythique: 3%
- Ile Légendaire: 0%

Plus vous avancerez dans le jeu, plus la probabilité d'avoir des iles plus rare augmentera.

- Vague 2:
    - Ile Commune: 54%
    - Ile Rare: 38%
    - Ile Mythique: 6%
    - Ile Légendaire: 2%

- Vague 3:
    - Ile Commune: 50%
    - Ile Rare: 36%
    - Ile Mythique: 10%
    - Ile Légendaire: 4%

- Vague 4:
    - Ile Commune: 47%
    - Ile Rare: 35%
    - Ile Mythique: 13%
    - Ile Légendaire: 5%

- Vague 5:
    - Ile Commune: 43%
    - Ile Rare: 33%
    - Ile Mythique: 17%
    - Ile Légendaire: 7%

- Vague 6:
    - Ile Commune: 38%
    - Ile Rare: 30%
    - Ile Mythique: 22%
    - Ile Légendaire: 10%

- Vague 7 et plus:
    - Ile Commune: 22%
    - Ile Rare: 33%
    - Ile Mythique: 30%
    - Ile Légendaire: 15%

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
Si vous souhaitez équiper l'objet, cliquez sur la touche 'A', qui fermera la fenêtre et vous équipera de l'objet. 
Au contraire, si vous ne souhaitez pas prendre l'objet, continuez votre chemin. L'équipement s'y trouvant pourra être récupéré par un ennemi, ou disparaitra au bout d'un certain temps.

Interface de choix des équipements:

![Interface de choix de bénédiction:](/data/images/Interfaces/equip_menu_item.png)


## __**Les bénédictions**__
Lorsque l'interface des bénédictions s'ouvrira quand vous serez à proximité d'une île, vous pourrez apercevoir l'icône symbolisant la bénédiction se trouvant sur l'île ainsi qu'une description de ses effets. Vous pourrez aussi trouver deux bulles numérotées '1' et '2'. Ces bulles sont vos espaces de stockages de bénédictions. '1' étant l'espace de stockage de votre bénédiction principale, et '2' l'espace de stockage de votre bénédiction secondaire.

Si vous souhaitez prendre la bénédiction se trouvant sur l'île, appuyer sur la touche du clavier (1 ou 2) à laquelle vous voulez assigner le déclenchement de la bénédiction. Notez qu'une bénédiction sur l'emplacement principal n'aura pas les mêmes effets que si elle est placée dans l'emplacement secondaire. 

Si au contraire, elle ne vous intéresse pas, continuez votre chemin. La bénédiction pourra être récupérée par un ennemi, ou disparaitra au bout d'un certain temps.
Vous pouvez avoir jusqu'à deux bénédictions en même temps, une principale et une secondaire.

Pour utiliser les bénédictions, utilisez le touche Z pour la bénédiction principale et E pour la bénédiction secondaire.
Entre chaque utilisation de bénédiction, il y a un cooldown plus ou moins long selon la bénédiction durant lequel vous ne pourrez pas l'utiliser.

Interface de choix de bénédiction:

![Interface de choix de bénédiction:](/data/images/Interfaces/equip_menu_bene.png)


## __**Les ennemis**__
Vous rencontrerez des ennemis durant votre partie. Ces ennemis sont comme vous: ils s'équipent et essayent de régner sur la mer.
Vous ferez face à des vagues d'ennemis de plus en plus coriaces allant d'un simple **Ennemi Basique**, à plusieurs **Ennemis Intelligents**.
Voici les spécificités des différents types d'ennemis:
- **Ennemi Basique:**
    Peut récupérer l'équipement sur les îles et attaque les navires à proximité

- **Ennemi Chasseur:**
    Ne peut pas récupérer d'équipement et poursuit le joueur pour le couler

- **Ennemi Intelligent:**
    Peut récupérer l'équipement sur les îles qui un meilleur équipement que leur équipement acutel, utilise les bénédictions et attaque les navires à proximité

Le bateau ennemi:

![Le bateau ennemi](/data/images/README/bateau.png)


## __**Les boss**__ (Fonctionnalité en développement - Non disponible)
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
- Equiper une bénédiction dans l'emplacement primaire: `1`
- Equiper une bénédiction dans l'emplacement secondaire: `2`
- Utiliser la bénédiciton primaire : `Z`
- Utiliser la bénédiciton secondaire : `E`

### Attention, lorsque vous avez la Coque Trouée (équipement malus), vos touches de déplacement seront inversées et deviendront les suivantes:
- Avancer: `Flèche Bas`
- Gauche: `Flèche Droite`
- Droite: `Flèche Gauche`

## __**Liste des équipement**__
**Wrecked Ocean** compte au total **23 pièces d'équipement**. 
Voici la liste de tous ces équiements triés par rareté, avec leur probabilités respectives ainsi que leurs effets.

- Equipement de base, obtensible seulement à l'apparition du joueur.
    - Coque de base
    - Canon de base
    - Voile de base

- Malus
    - Coque:
        - Coque Trouée (6,66%) - Malus - Inverse les commandes de déplacement


            ![Coque Trouée](/data/images/README/coque_malus.png)
        
        - Canons Rouillés (6,66%) - Malus - Rend les projectiles 25% plus lents

            
            ![Canons Rouillés](/data/images/README/canon_malus.png)

        - Voile Trouée (6,66%) - Malus - Diminue la vitesse maximale du joueur de 20%


            ![Voile Trouée](/data/images/README/voile_malus.png)


- Commun
    - Coques:

        ![Coque Commune](/data/images/README/coque_commun.png)

        - Coque chêne (20%) - Augmente la vitesse maximale de 5%
        - Coque épicéa (10%) - Ajoute 10 à la santé maximale du joueur

    - Canons:

        ![Canons Communs](/data/images/README/canon_commun.png)

        - +1 Canon (10%) - Ajoute un canon à l'avant
        - Canon en bronze (20%) - Ajoute 20% de dégâts aux projectiles

    - Voiles:

        ![Voile Commune](/data/images/README/voile_commune.png)

        - Voile en toile de jute (20%) - Augmente la vitesse maximale de 5%
        

- Rare
    - Coques:

        ![Coque Rare](/data/images/README/coque_rare.png)

        - Coque en bouleau (10%) - Ajoute 10 à la santé maximale du joueur et augmente la vitesse maximale de 5%
        - Coque en chêne massif (10%) - Ajoute 75 à la santé maximale du joueur

    - Canons:
    
        ![Canons Rares](/data/images/README/canon_rare.png)

        - +2 Canons (10%) - Ajoute un canon à l'avant et à l'arrière
        - Canon en argent (17,5%) - Ajoute 33% de dégats  et 5% de vitesse aux projectiles
        - Canon Ballistique (10%) - Multiplie la distance maximale des projectiles par 2
    - Voiles:

        ![Voile Rare](/data/images/README/voile_rare.png)

        - Voile Latine (17,5%) - Augmente la vitesse maximale de 10%

- Mythique
    - Coques:

        ![Coque Mythique](/data/images/README/coque_mythique.png)

        - Coque en bois magique (12%) - Ajoute 50 à la santé maximale du joueur  et augmente la vitesse maximale de 20% et à une chance de 20% de ne pas se prendre les dégâts
    
    - Canons:
    
        ![Canons Mythiques](/data/images/README/canon_mythique.png)

        - +3 Canons (12%) - Ajoute un canon à l'avant, à l'arrière et dans la diagonale avant droite du bateau
        - Canon en or (12%) - Ajoute 66% de dégats et 10% de vitesse au projectiles et augmente la cadence de tir de 10%
        - Canon à tirs doubles (12%) - Tire un deuxième projectile après chaque tir

    - Voiles:

        ![Voile Mythique](/data/images/README/voile_mythique.png)

        - Voile enchantée (12%) - Augmente le vitesse maximale de 25% et augmente la maniabilité de 2%

- Légendaire
    - Coques:

        ![Coque Légendaire](/data/images/README/coque_legendaire.png)

        - Coque légendaire (12,5%) - Ajoute 60 à la santé maximale du joueur  et augmente la vitesse maximale de 30%

    - Canons:
    
        ![Canons Légendaires](/data/images/README/canon_legendaire.png)

        - +4 Canons (12,5%) - Ajoute un canon à l'avant, à l'arrière et dans les deux diagonales à l'avant du bateau
        - Canon légendaire (12,5%) - Ajoute 133% de dégats et 15% de vitesse au projectiles et augmente la cadence de tir de 10%

    - Voiles:

        ![Voile Légendaire](/data/images/README/voile_legendaire.png)

        - Voile légendaire (12,5%) - Augmente le vitesse maximale de 30% et augmente la maniabilité de 5%

        
## __**Liste des bénédictions**__
**Wrecked Ocean** compte au total **8 bénédictions**. 
Voici la liste de tous ces bénédicitons triées par rareté, avec leur probabilités respectives ainsi que leurs effets.

- __**Rare**__

    - __Bénédiction Dash__ (12,5%) (Cooldown - 15 sec)

        ![Bénédiction Dash](/data/images/README/beneDash.png)

        - Emplacement Principal - Permet au joueur de se propulser vers l'avant de manière considérable
        - Emplacement Secondaire - Permet au joueur de se propulser vers l'avant de manière plutôt efficace
      
    - __Bénédiction Santé__ (12,5%) (Cooldown - 40 sec)

        ![Bénédiction Santé](/data/images/README/beneSante.png)

        - Emplacement Principal - Permet au joueur de restaurer 50% de ses points de vie max
        - Emplacement Secondaire - Permet au joueur de restaurer 25% de ses points de vie max

- __**Mythique**__

    - __Bénédiction d'Aura__ (20%) (Cooldown - 30sec)

        ![Bénédiction d'Aura](/data/images/README/beneAura.png)

        - Emplacement Principal - Crée une zone autour du joueur qui infligera entre 2 et 10 dégats aux ennemis en fonction de leur proximité
        - Emplacement Secondaire - Crée une zone autour du joueur qui infligera entre 1 et 5 dégats aux ennemis en fonction de leur proximité
    
    - __Bénédiction de Rage__ (20%) (Cooldown - 30sec)

        ![Bénédiction de Rage](/data/images/README/beneRage.png)

        - Emplacement Principal - Augmente les dégats et la vitesse du joueur (+50%) pendant 10 sec, mais le limite temporairement à 30 pts de vie
        - Emplacement Secondaire - Augmente les dégats et la vitesse du joueur (+50%) pendant 5 sec, mais le limite temporairement à 20 pts de vie

- __**Légendaire**__

    - __Bénédiction Godmode__ (25%) (Cooldown - 40sec)

        ![Bénédiction GodMode](/data/images/README/beneGodMode.png)

        - Emplacement Principal - Permet au joueur de ne pas prendre de dégats pendant 10 sec
        - Emplacement Secondaire - Permet au joueur de ne pas prendre de dégats pendant 5 sec
      
    - __Bénédiction Projectiles__ (25%) (Cooldown - 50sec)

        ![Bénédiction Projectiles](/data/images/README/beneProjectiles.png)

        - Emplacement Principal - Permet au joueur d'envoyer une horde de projectile autour de lui quand il tire pendant 10 sec (tir double)
        - Emplacement Secondaire - Permet au joueur d'envoyer une horde de projectile autour de lui quand il tire pendant 10 sec (tir simple)

# Informations Complémentaires

## __**Crédits**__
**Wrecked Ocean** est un jeu réalisé à l'occasion du concours Trophée NSI, dans la catégorie Terminale.
Notre professeur, M. MARIE-JEANNE nous a accompagné pendant toute la durée de ce projet, nous apportant solutions et idées nouvelles.
Voici la liste des différents rôles et des élèves ayant participé au projet.

- Réalisation:
    - BELEC-ESCALERA Elliot
    - CADEAU--FLAUJAT Gabriel

- Développement:
    - BELLEC-ESCALERA Elliot (Bénédictions, Base du jeu et UI)
    - CADEAU--FLAUJAT Gabriel (Equipements, Interfaces, Iles et UI)
    - KELEMEN Thomas (Navires ennemis)
    - GABRIEL Tom (UI et Animations)

- Textures:
    - BELLEC-ESCALERA Elliot (Indicateurs de bénédictions et Icones)
    - CADEAU--FLAUJAT Gabriel (Interfaces, Icones de bénédictions, Bateaux et Iles)
    - GABRIEL Tom (Icones des équipements)

- Documentation:
    - GABRIEL Tom (README, Présentation PDF, Documents d'explication, Résumé)
    - CADEAU--FLAUJAT Gabriel (README, Commentaires, Docstring)
    - BELLEC-ESCALERA Elliot (Commentaires, Docstring)
    - KELEMEN Thomas (Commentaires, Docstring)

- Réalisation Vidéo:
    - GABRIEL Tom (Montage, VFX, 3D)
    - CADEAU--FLAUJAT Gabriel (Voix Off, Gameplay)

- Remerciements supplémentaires:
    - PLADEAU Quentin (Aide au développement)
    - FreePik (Ressources)
