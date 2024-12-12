from random import choices, randint

class Iles:
    def __init__(self):
        self.ile_rarete = ['commun', 'rare','mythique', 'légendaire']

        self.liste_recompenses_communes = ['1_canon', 'canon_en_bronze', 'voile_toile_de_jute', 'coque_epicea', 'coque_chene', self.random_malus(), 'rien']
        self.probabilité_commun = [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3]

        self.liste_recompenses_rares = ['2_canons', 'canon_en_argent', 'canon_balistique', 'voile_latine', 'coque_bouleau', 'coque_chene_massif', self.random_malus(), 'rien', 'bene_dash', 'bene_sante']
        self.probabilité_rare = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.1, 0.125, 0.125]

        self.liste_recompenses_mythiques = ['3_canons', 'canon_en_or', 'canon_tir_double', 'voile_enchantee', 'coque_bois_magique', 'bene_aura', 'bene_rage']
        self.probabilité_mythique = [0.12, 0.12, 0.12, 0.12, 0.12, 0.2, 0.2]
    
        self.liste_recompenses_legendaires = ['4_canons', 'canon_legendaire', 'voile_legendaire', 'coque_legendaire', 'bene_godmode', 'bene_projectile']
        self.probabilité_legendaire = [0.125, 0.125, 0.125, 0.125, 0.25, 0.25]
        
        self.dict_iles = {
            'commun' : self.probabilité_commun, 
            'rare' : self.probabilité_rare,
            'mythique' : self.probabilité_mythique, 
            'légendaire': self.probabilité_legendaire}

        self.position_x = None
        self.position_y = None

    def type_ile(self):
        self.typeList = choices(self.ile_rarete, weights=[0.55, 0.30, 0.14, 0.01], k=1)
        self.type = self.typeList[0]
        print(self.type)
        return self.type


    def random_malus(self):
        self.malus = [
            "canons_rouilles",
            "toile_trouee",
            "coque_trouee"
        ]
        a = choices(self.malus)
        return a

    def type_recompenses(self):
        self.weights = self.dict_iles[self.type]
        if self.type == 'légendaire':
            self.liste_recompenses = self.liste_recompenses_legendaires
        elif self.type == 'mythique':
            self.liste_recompenses = self.liste_recompenses_mythiques
        elif self.type == "rare":
            self.liste_recompenses = self.liste_recompenses_rares
        elif self.type == "commun":
            self.liste_recompenses = self.liste_recompenses_communes

        self.recompenseListe = choices(self.liste_recompenses, weights=self.weights, k=1)
        self.recompense = self.recompenseListe[0]
        print(self.recompense)



    def position(self):
        """appartition aléatoire sur la map"""
        self.position_x = randint(-400,400)
        self.position_y = randint(-400,400)


    def apparition(self):
        """appartition régulière"""
        pass

coucou = Iles()

coucou.type_ile()
coucou.type_recompenses()
