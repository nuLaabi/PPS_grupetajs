import interface_manager as IM
import database_manager as DM
from classes import *


file = open("izvade.txt", 'w', encoding="utf-8")
planojums = Planojums("test")
DM.ielasitKlientuDatus("datasheet.csv", planojums)
DM.saglabatPlanojumu(planojums)
planojums = {"kautkas": "navkartiba"}
planojums = DM.iegutPlanojumu("test")
for a,b in planojums.KlientuDati.items():
    file.write(a + ": [" + ", ".join(b) + "]\n")
file.close()