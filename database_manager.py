import csv
import _pickle
from classes import *
import os

def visiPlanojumi():
    '''
    Funkcija, kas atgriež sarakstu ar visu plānojumu nosaukumiem skatoties pēc Plānojumu mapes datnēm, tā neņem pretī argumentus un atgriež sarakstu ar string vērtībām.
    '''
    path = "Plānojumi"
    planojumi = []
    datnes = os.listdir(path)
    for datne in datnes:
        if os.path.isfile(os.path.join(path, datne)):
            planojumi.append(datne)
    return planojumi
def iegutPlanojumu(nosaukums):
    '''
    Funkcija, kas pēc plānojuma nosaukuma iegūst no attiecīgā plānojuma datnes datus un atgriež Planojums klases objektu

    :param nosaukums: Nosaukums plānojumam, kuru vēlas iegūt, string vērtība
    '''
    plan = _pickle.load(open(f"Plānojumi/{nosaukums}.bin", "rb"))
    planojums = planojumsNoVardnicas(plan)
    return planojums
def saglabatPlanojumu(planojums):
    '''
    Funkcija plānojuma saglabāšanai, tā saņem pretī Planojums klases objektu un pārveido to par vārdnīcu, kura tiek ar pickle moduli serializēta binārā datnē Plānojumi mapē.
    
    :param planojums: Plānojums, kuru vēlas saglabāt, Planojums klases objekts
    '''
    _pickle.dump(planojums.uzVardnicu(), open(f"Plānojumi/{planojums.Nosaukums}.bin", "wb"))
def dzestPlanojumu(nosaukums):
    '''
    Funkcija plānojuma dzēšanai. Dzēš plānojuma datni no Plānojumi mapes.
    
    :param nosaukums: Plānojuma nosaukums, kuru vēlas dzēst, string vērtība
    :raises: FileNotFoundError ja fails neeksistē
    :raises: PermissionError ja nav tiesību dzēst failu
    '''
    ceļš = f"Plānojumi/{nosaukums}.bin"
    if not os.path.exists(ceļš):
        raise FileNotFoundError(f"Plānojums '{nosaukums}' neeksistē")
    os.remove(ceļš)
def ielasitKlientuDatus(path, planojums):
    '''
    Funkcija, kas no csv datnes ielasa klientu anketu datus un saglabā programmai nepieciešamo informāciju Planojums klases objektā.
    
    :param path: csv datnes atrašanās vieta datņu struktūrā, string vērtība
    :param planojums: plānojums, kurā tiks glabāti ielasītie dati, Planojums klases objekts
    '''
    tabula = []
    ds = planojums.DatnesStruktura
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
            kursi = line[ds["kursi"]]
            fil = line[ds["filiales"]]
            pirm = line[ds["laikiPirmdiena"]]
            otr = line[ds["laikiOtrdiena"]]
            tres = line[ds["laikiTrešdiena"]]
            ceturt = line[ds["laikiCeturtdiena"]]
            piekt = line[ds["laikiPiektdiena"]]
            sest = line[ds["laikiSestdiena"]]
            laiki = laikuStrukturetajs(pirm, otr, tres, ceturt, piekt, sest)
            kurss = kursi.split(", ")
            fil = fil.split(", ")
            audzeknis = Audzeknis(vards+" "+uzvards, persKods, laiki, fil, kurss, telNr, epasts)
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


