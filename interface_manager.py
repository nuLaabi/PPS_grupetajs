import tkinter as tk
from tkinter.constants import *
from classes import *
import database_manager as DM
def atvertPlanojumu(datnesNosaukums, planojumuLapa):
    '''
    Palīgfunkcija grupu skata atvēršanai no plānojumu izvēles skata. Tā ņem kā parametrus atveramā plānojuma datnes nosaukumu un plānojumu izvēles lapas objektu, lai plānojumu izvēles lapu aizvērtu.
    
    :param datnesNosaukums: Nosaukums plānojuma datnei, no kuras ielasīs datus un attēlos grupu skatā, string vērtība.
    :param planojumuLapa: Plānojuma izvēles lapas objekts, lai aizvērtu izvēles lapu.
    '''
    nosaukums = "".join(datnesNosaukums.split('.')[:-1:])
    planojumuLapa.destroy()
    GrupuSkats(DM.iegutPlanojumu(nosaukums))
def GrupuSkats(planojums):
    '''
    Funkcija, kas rada Grupu kopskata skatu
    
    :param planojums: Plānojums, kura dati tiek attēloti skatā, Planojums klases objekts
    '''
    root = tk.Tk()
    root.title("Grupas")
    root.geometry("1920x1080")
    group_view = tk.Frame(root, anchor="w", width="30%")
    group_view.grid(column=0, row=0)
    index = 0
    for grupa in planojums.Grupas:
        poga = tk.Button(group_view, anchor="we", text=grupa.Kods)
        poga.grid(column=0, row=index)
        index += 1
    tk.mainloop()
def PlanojumuSkats():
    '''
    Funkcija, kas attēlo visu Plānojumu nosaukumus, ielasot tos no Plānojumi mapes, un ļauj atlasīt plānojumu.
    '''
    root = tk.Tk()
    root.title("Plānojumi")
    root.geometry("1920x1080")
    planojumi = DM.visiPlanojumi()
    planojumu_skats = tk.Frame(root)
    planojumu_skats.grid(column=0, row=0)
    index = 0
    for plan in planojumi:
        poga = tk.Button(planojumu_skats, anchor="center", text=plan, command=lambda plan=plan: atvertPlanojumu(plan, root))
        poga.grid(column=0, row=index)
        index += 1
    tk.mainloop()




