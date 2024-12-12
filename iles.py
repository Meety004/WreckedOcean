from random import choices, randint

class Iles:
    def __init__(self):
        self.ile_rarete = ['commun', 'rare', 'légendaire', 'mythique']

        self.liste_recompenses_communes = ['1_canon', 'canon_en_bronze', 'voile_toile_de_jute', 'coque_epicea', 'coque_chene', self.random_malus(), 'rien']
        self.probabilité_commun = [0.60, 0.35, 0.04, 0.005, 0.005]

        self.liste_recompenses_rares = ['2_canons', 'canon_en_argent', 'canon_balistique', 'voile_latine', 'coque_bouleau', 'coque_chene_massif', self.random_malus(), 'rien']
        self.probabilité_rare = [0.50,0.40, 0.07, 0.015, 0.015]

        self.liste_recompenses_:mythiques = ['3_canons', 'canon_en_or', 'canon_tir_double', 'voile_enchantee', 'coque_bois_magique']
        self.probabilité_mythique = [0.35,0.35,0.20,0.10,0.10]
    
        self.liste_recompenses_rare = ['2_canons', 'canon_en_argent', 'canon_balistique', 'voile_latine', 'coque_bouleau', 'coque_chene_massif', self.random_malus(), 'rien']
        self.probabilité_legendaire = [0.40, 0.40, 0.10, 0.5, 0.5]
        
        self.dict_iles = {'commun' : self.probabilité_commun, 'rare' : self.probabilité_rare, 'légendaire': self.probabilité_legendaire, 'mythique' : self.probabilité_mythique}
        self.position_x = None
        self.position_y = None

    def type_ile(self):
        self.type = choices(self.ile_rarete,weights=[0.55,0.4,0.04,0.01], k=1)
        print(self.type)

    def random_malus(self):
        self.malus = [
            "canons_rouilles",
            "toile_trouee",
            "coque_trouee"
        ]
        a = random.choices(self.malus)
        return a

    def type_recompenses(self):
        self.type_ile()
        a = self.dict_iles[self.type[0]]
        self.recompenses = choices(self.liste_recompenses,weights=a, k=1)
        print(self.recompenses)


    def position(self):
        """appartition aléatoire sur la map"""
        self.position_x = randint(-400,400)
        self.position_y = randint(-400,400)


    def apparition(self):
        """appartition régulière"""
        pass

coucou = Iles()
coucou.type_recompenses()
