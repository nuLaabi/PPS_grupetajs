import interface_manager as IM
import database_manager as DM
from classes import *


file = open("izvade.txt", 'w', encoding="utf-8")
planojums = Planojums("test")
DM.ielasitKlientuDatus("datasheet.csv", planojums)
generetAudzeknus(300, planojums)
planojums.generetGrupas()
DM.saglabatPlanojumu(planojums)
planojums = DM.iegutPlanojumu("test")
file.close()
IM.PlanojumuSkats()