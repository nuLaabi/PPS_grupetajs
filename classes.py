import random
SEED = 0
random.seed(SEED)


def laiki():
    Laiki = { # Pieejamie nodarbību laiki tiks šādi glabāti, atslēgas ir nedēļas dienas kārtas numurs, piemēram, pie atslēgas 1 ir glabāta informācija par pirmdienu, tālāk katra iekšējā atslēga attiecas uz laiku pēc kārtas tajā dienā, tā kā sestdien ir 2 reizes vairāk nodarbību, tad tur arī ir vairāk datu
        1: {1: True, 2: True, 3: True}, # laika indeksi 0, 1, 2
        2: {1: True, 2: True, 3: True}, # laika indeksi 3, 4, 5
        3: {1: True, 2: True, 3: True}, # laika indeksi 6, 7, 8
        4: {1: True, 2: True, 3: True}, # laika indeksi 9, 10, 11
        5: {1: True, 2: True, 3: True}, # laika indeksi 12, 13, 14
        6: {1: True, 2: True, 3: True, 4: True, 5: True, 6: True} # laika indeksi 15, 16, 17, 18, 19, 20
    }
    return Laiki.copy()
def indeksuLicejs(klientuNelaiki, diena):
    laiki = klientuNelaiki.split(", ")
    if len(diena) == 3:
        for laiks in laiki:
            if laiks == "16:00 - 17:20":
                diena[1] = False
            elif laiks == "17:30 - 18:50":
                diena[2] = False
            elif laiks == "19:00 - 20:20":
                diena[3] = False
    else:
        for laiks in laiki:
            if laiks == "10:00 - 11:20":
                diena[1] = False
            elif laiks == "11:30 - 12:50":
                diena[2] = False
            elif laiks == "13:00 - 14:20":
                diena[3] = False
            elif laiks == "15:00 - 16:20":
                diena[4] = False
            elif laiks == "16:30 - 17:50":
                diena[5] = False
            elif laiks == "18:00 - 19:20":
                diena[6] = False


def laikuStrukturetajs(pirm, o, t, c, piekt, s):
    l = laiki()
    indekss = 1
    for diena in [pirm, o, t, c, piekt, s]:
        indeksuLicejs(diena, l[indekss])
        indekss += 1
    return l

Kursi = {
        "Scratch pamati" : "SCR1", 
        "Scratch padziļināti" : "SCR2",
        "Mobilo lietotņu izstrāde" : "APPS", 
        "Mājaslapu izstrādes pamati" : "WEB1", 
        "Mājaslapu izstrāde padziļināti" : "WEB2", 
        "Python pamati" : "PYT1", 
        "Python padziļināti" : "PYT2", 
        "C++ pamati" : "C++1", 
        "C++ padziļināti" : "C++2", 
        "Java pamati" : "JAVA", 
        "Sporta programmēšana (C++)" : "C++3", 
        "Olimpiāžu programmēšana (C++)" : "C++4",
        "Programmēšana ar MI (C++)": "C+MI",
        "3D spēļu programmēšana": "GAME"
}
def kursaKods(nosaukums):
    return Kursi.get(nosaukums, "ERROR_KURSS_NEEKSISTĒ")
def laikaIndeksaTulkotajs(laikaIndekss): # funkcija laika indeksa konvertēšanai par dienu un laiku
    diena = laikaIndekss // 3 + 1
    laiks = laikaIndekss % 3 + 1
    if diena == 7: # tā kā sestdien ir 2 reizes vairāk nodarbību laiku, matemātiski tās otrā puse izskatās kā 7. diena, attiecīgi jāpielāgo laika un dienas numurs
        diena = 6
        laiks += 3
    return (diena, laiks)
def dienasLaikaTulkotajs(diena, laiks): # funkcija, kas pārveido dienas un laika numurus par laika indeksu
    return (diena - 1) * 3 + laiks - 1
def grupasKods(fil, laikaIndekss, kurss):
    dienaLaiks = laikaIndeksaTulkotajs(laikaIndekss)
    kods = filialesBurts(fil) + "-" + str(dienaLaiks[0]) + "-" + str(dienaLaiks[1]) + "-" + kursaKods(kurss) #potenciāli būs problēmas ar filiāles burtu Āgenskalnam
def filialesBurts(nosaukums):
    filiales = {
        "Centra (Dagdas iela 4)" : "C", 
        "Āgenskalna (Kalnciema iela 7A)" : "A", 
        "Teikas (Zemgaļu iela 8)" : "T", 
        "Tiešsaistes nodarbības" : "O"
    }
    return filiales.get(nosaukums, "ERROR_FILIĀLE_NEEKSISTĒ")
class Persona:
    def __init__(self, vards, persKods, laiki, fil, kursi, telNr, epasts):
        self.Vards = vards
        self.PersKods = persKods
        self.Laiki = laiki # informācija par pieejamajiem laikiem
        self.Filiales = fil # saraksts ar filiālēm
        self.Kursi = kursi # saraksts ar kursiem
        self.TelNr = telNr
        self.Epasts = epasts
        
    def laiksPieejams(self, diena, laiks=-1): # funkcija pieejamības pārbaudīšanai, diena atbild par nedēļas dienu un laiks par nodarbības laiku sakārtotu pēc kārtas hronoloģiski, ja tiek ievadīta tikai diena, tad tas tiek uztverts par laika indeksu
        if laiks == -1:
            dienaLaiks = laikaIndeksaTulkotajs(diena)
            return self.Laiki[dienaLaiks[0]][dienaLaiks[1]]
        return self.Laiki[diena][laiks]
    
    def grupaDeriga(self, fil, laikaIndekss, kurss):
        return fil in self.Filiales and self.laiksPieejams(laikaIndekss) and kurss in self.Kursi
    def uzVardnicu(self):
        vardnica = {
            "vards": self.Vards,
            "persKods": self.PersKods,
            "laiki": self.Laiki,
            "filiales": self.Filiales,
            "kursi": self.Kursi,
            "telNr": self.TelNr,
            "epasts": self.Epasts,
        }
        return vardnica
class Audzeknis(Persona):
    def __init__(self, vards, persKods, laiki, fil, kursi, telNr, epasts):
        super().__init__(vards, persKods, laiki, fil, kursi, telNr, epasts)
        laikuSkaits = 0
        for diena in self.Laiki:
            laikuSkaits += len(self.Laiki[diena])
        self.Pieejamiba = laikuSkaits * len(self.Filiales) * len(self.Kursi)
        self.Komplektets = False
    def uzVardnicu(self):
        vardnica = {
            "vards": self.Vards,
            "persKods": self.PersKods,
            "laiki": self.Laiki,
            "filiales": self.Filiales,
            "kursi": self.Kursi,
            "telNr": self.TelNr,
            "epasts": self.Epasts,
            "pieejamiba": self.Pieejamiba,
            "komplektets": self.Komplektets
        }
        return vardnica
class Grupa:
    def __init__(self, fil, laikaIndekss, kurss, audzekni=[], skolotajs=None):
        self.Filiale = fil
        self.Laiks = laikaIndekss
        self.Kurss = kurss
        self.Audzekni = audzekni
        self.Skolotajs = skolotajs
        self.Komplekteta = False
        self.Kods = grupasKods(fil, laikaIndekss, kurss)
        self.AudzeknuSkaits = len(self.Audzekni)
        self.Vertejums = 0
    def pievienotAudzekni(self, audzeknis):
        self.Audzekni.append(audzeknis)
    def pieder(self, audzeknis):
        return audzeknis in self.Audzekni
    def rekinatVertibu(self, koeficienti):
        pass
    def uzVardnicu(self):
        audzekni = []
        for audzeknis in self.Audzekni:
            audzekni.append(audzeknis.uzVardnicu())
        vardnica = {
            "filiale": self.Filiale,
            "laiks": self.Laiks,
            "kurss": self.Kurss,
            "audzekni": audzekni,
            "skolotajs": self.Skolotajs.uzVardnicu() if self.Skolotajs else None,
            "komplekteta": self.Komplekteta,
            "Kods": self.Kods,
            "audzeknuSkaits": self.AudzeknuSkaits,
            "vertejums": self.Vertejums
        }
        return vardnica

class Planojums:
    def __init__(self, nosaukums):
        self.Nosaukums = nosaukums
        self.Grupas = {}
        self.Audzekni = []
        self.Skolotaji = []
        self.KlientuDati = {
            "vardi": [],
            "uzvardi": [],
            "persKodi": [],
            "telNr": [],
            "epasti": [],
            "kursi": [],
            "filiales": [],
            "laikiPirmdienas": [],
            "laikiOtrdienas": [],
            "laikiTrešdienas": [],
            "laikiCeturtdienas": [],
            "laikiPiektdienas": [],
            "laikiSestdienas": [],
        }
        self.Koeficienti = {
            "blakusNodarbiba": 0,
            "skolenuPieejamiba": 0,
            "kursaNeesamiba": 0,
            "opcijuNeesamiba": 0
        }
        self.DatuStruktura = {
            "vards": 1,
            "uzvards": 2,
            "persKods": 4,
            "telNr": 5,
            "epasts": 6,
            "kurss": 7,
            "filiales": 8,
            "laikiPirmdiena": 9,
            "laikiOtrdiena": 10,
            "laikiTrešdiena": 11,
            "laikiCeturtdiena": 12,
            "laikiPiektdiena": 13,
            "laikiSestdiena": 14
        }
    def pievienotAudzekni(self, audz):
        self.Audzekni.append(audz)
    def pievienotGrupu(self, grupa):
        self.Grupas.append(grupa)
    def generetGrupas(self):
        for audzeknis in self.Audzekni:
            for filiale in audzeknis.Filiales:
                for diena,laiks in audzeknis.Laiki.items():
                    kods = grupasKods(filiale, dienasLaikaTulkotajs(diena,laiks), audzeknis.Kursi[0])
                    if kods in self.Grupas:
                        self.Grupas[kods].AudzeknuSkaits += 1
                        self.Grupas[kods].pievienotAudzekni[audzeknis]
                    else:
                        self.Grupas[kods] = Grupa(filiale, dienasLaikaTulkotajs(diena,laiks), audzeknis.Kursi[0], [audzeknis])
                    
                    
    def atjaunotGrupas(self, komplektetaGrupa):
        '''
        Metode potenciālo grupu atjaunošanai. Potenciālo grupu saraksts ir jāatjaunina kādas grupas komplektēšanas gadījumā, tādēļ tiek padots Grupa klases objekts, kas norāda, kura grupa tika komplektēta.
        
        :param komplektetaGrupa: Grupa klases objekts, norāda, kura grupa tika komplektēta.
        '''
        for grupa in self.Grupas.values():
            if not grupa.Komplekteta:
                veiktasIzmainas = False
                for audzeknis in komplektetaGrupa.Audzekni:
                    if audzeknis in grupa.Audzekni:
                        veiktasIzmainas = True
                        grupa.Audzekni.remove(audzeknis)
                if grupa.Skolotajs == komplektetaGrupa.Skolotajs or grupa.Laiks == komplektetaGrupa.Laiks or grupa.Kurss == komplektetaGrupa.Kurss or grupa.Filiale == komplektetaGrupa.Filiale:
                    veiktasIzmainas = True
                if veiktasIzmainas:
                    grupa.rekinatVertibu(self.Koeficienti)
    def uzVardnicu(self):
        grupas = []
        for grupa in self.Grupas.values():
            grupas.append(grupa.uzVardnicu())
        audzekni = []
        for audzeknis in self.Audzekni:
            audzekni.append(audzeknis.uzVardnicu())
        vardnica = {
            "nosaukums": self.Nosaukums,
            "grupas": grupas,
            "audzekni": audzekni,
            "klientuDati": self.KlientuDati,
            "koeficienti": self.Koeficienti,
            "datuStruktura": self.DatuStruktura
        }
        return vardnica
def generetAudzeknus(skaits, planojums):
    vardi = ["Jānis", "Pēteris", "Ēriks", "Ansis", "Artūrs", "Marks", "Jēkabs", "Antons", "Roberts", "Toms"]
    uzvardi = ["Bērziņš", "Eglīts", "Kalniņš", "Mežs", "Kļaviņš", "Ezers", "Nauda", "Pūpols", "Dīķis", "Spainis"]
    kursi = ["Scratch pamati", "Scratch padziļināti", "Mobilo lietotņu izstrāde", "Mājaslapu izstrādes pamati", "Mājaslapu izstrāde padziļināti", "Python pamati", "Python padziļināti", "C++ pamati", "C++ padziļināti", "Java pamati", "Sporta programmēšana (C++)", "Olimpiāžu programmēšana (C++)"]
    filiāles = ["Centra (Dagdas iela 4)", "Āgenskalna (Kalnciema iela 7A)", "Teikas (Zemgaļu iela 8)", "Tiešsaistes nodarbības"]
    for i in range(skaits):
        vards = random.choice(vardi) + " " + random.choice(uzvardi)
        kurss = random.choice(kursi)
        filIndekss = random.randint(0, 3)
        if random.random() < 0.3:
            fil = [filiāles[filIndekss], filiāles[(filIndekss+random.randint(1,3))%4]]
        else:
            fil = [filiāles[filIndekss]]
        laiki = laiki()
        for diena in laiki:
            if random.random() > 0.35:
                for laiks in diena:
                    if random.random() > 0.35:
                        laiki[diena][laiks] = True
        persKods = str(random.randint(100000, 999999)) + '-' + str(random.randint(100000, 999999))
        telNr = str(random.randint(0, 99999999))
        epasts = f"skolens{i}@gmail.com"
        skolens = Persona(vards, persKods, laiki, fil, [kurss], telNr, epasts)
        planojums.pievienotAudzekni(skolens)



