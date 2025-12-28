import csv
import _pickle
from classes import *
'''
AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
'''
def iegutPlanojumu(nosaukums):
    planojums = Planojums(nosaukums)
    plan = _pickle.load(open(f"Plānojumi/{nosaukums}.bin", "rb"))
    planojums.Nosaukums = plan["nosaukums"]
    planojums.Grupas = plan["grupas"]
    planojums.Audzekni = plan["audzekni"]
    planojums.KlientuDati = plan["klientuDati"]
    planojums.Koeficienti = plan["koeficienti"]
    planojums.DatuStruktura = plan["datuStruktura"]
    return planojums
def saglabatPlanojumu(planojums):
    plan = {
        "nosaukums": planojums.Nosaukums,
        "grupas": planojums.Grupas,
        "audzekni": planojums.Audzekni,
        "klientuDati": planojums.KlientuDati,
        "koeficienti": planojums.Koeficienti,
        "datuStruktura": planojums.DatuStruktura
    }
    _pickle.dump(plan, open(f"Plānojumi/{planojums.Nosaukums}.bin", "wb"))
#
def ielasitKlientuDatus(path, planojums):
    tabula = []
    ds = planojums.DatuStruktura
    kd = planojums.KlientuDati
    with open(path, newline='', encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f)
        for line in reader:
            tabula.append(line)
            vards = line[ds["vards"]]
            uzvards = line[ds["uzvards"]]
            persKods = line[ds["persKods"]]
            telNr = line[ds["telNr"]]
            epasts = line[ds["epasts"]]
            kurss = line[ds["kurss"]]
            fil = line[ds["filiales"]]
            pirm = line[ds["laikiPirmdiena"]]
            otr = line[ds["laikiOtrdiena"]]
            tres = line[ds["laikiTrešdiena"]]
            ceturt = line[ds["laikiCeturtdiena"]]
            piekt = line[ds["laikiPiektdiena"]]
            sest = line[ds["laikiSestdiena"]]
            laiki = laikuStrukturetajs(pirm, otr, tres, ceturt, piekt, sest)
            audzeknis = Persona(vards+" "+uzvards, persKods, laiki, fil, [kurss], telNr, epasts)
            planojums.pievienotAudzekni(audzeknis)
            kd["vardi"].append(vards)
            kd["uzvardi"].append(uzvards)
            kd["persKodi"].append(persKods)
            kd["telNr"].append(telNr)
            kd["epasti"].append(epasts)
            kd["kursi"].append(kurss)
            kd["filiales"].append(fil)
            kd["laikiPirmdienas"].append(pirm)
            kd["laikiOtrdienas"].append(otr)
            kd["laikiTrešdienas"].append(tres)
            kd["laikiCeturtdienas"].append(ceturt)
            kd["laikiPiektdienas"].append(piekt)
            kd["laikiSestdienas"].append(sest)
    return tabula
#


