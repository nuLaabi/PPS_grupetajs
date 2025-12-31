import tkinter as tk
from tkinter import ttk, messagebox, font
import database_manager as DM
def atvertPlanojumu(nosaukums, planojumuLapa):
    '''
    Palīgfunkcija grupu skata atvēršanai no plānojumu izvēles skata. Tā ņem kā parametrus atveramā plānojuma nosaukumu un plānojumu izvēles lapas objektu, lai plānojumu izvēles lapu aizvērtu.
    
    :param nosaukums: Nosaukums plānojumam, no kura datnes ielasīs datus un attēlos grupu skatā, string vērtība.
    :param planojumuLapa: Plānojuma izvēles lapas objekts, lai aizvērtu izvēles lapu.
    '''
    planojumuLapa.destroy()
    GrupuSkats(DM.iegutPlanojumu(nosaukums))
def GrupuSkats(planojums):
    '''
    Funkcija, kas rada Grupu kopskata skatu
    
    :param planojums: Plānojums, kura dati tiek attēloti skatā, Planojums klases objekts
    '''
    root = tk.Tk()
    root.title("Grupas")
    root.geometry("900x600")
    lapa = ttk.Frame(root, padding=12)
    lapa.pack(fill='both', expand=True)
    ttk.Label(lapa, text="Plānojums " + planojums.Nosaukums, font=font.Font(size=16, weight="bold")).pack(anchor="w")
    container = ttk.Frame(lapa)
    container.pack(fill='both', expand=True, pady=8)
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable = ttk.Frame(canvas)
    scrollable.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0,0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    for grupa in planojums.Grupas:
        lbl = ttk.Label(scrollable, text=grupa, padding=(6,6))
        lbl.pack(fill='x', pady=2)
    ttk.Button(lapa, text="Aizvērt", command=root.destroy).pack(anchor="e", pady=(8,0))
    root.mainloop()
def PlanojumuSkats():
    '''
    Funkcija, kas attēlo visu Plānojumu nosaukumus, ielasot tos no Plānojumi mapes, un ļauj atlasīt plānojumu.
    '''
    root = tk.Tk()
    root.title("Plānojumi")
    root.geometry("800x600")
    lapa = ttk.Frame(root, padding=12)
    lapa.pack(fill='both', expand=True)
    ttk.Label(lapa, text="Izvēlies plānojumu", font=font.Font(size=18, weight="bold")).pack(anchor="center")

    mekletais = tk.StringVar()
    meklesanas_sadala = ttk.Frame(lapa)
    meklesanas_sadala.pack(fill='x', pady=(8, 6))
    ttk.Label(meklesanas_sadala, text="Meklēt:").pack(side='left', padx=(0,6))
    meklesanas_lauks = ttk.Entry(meklesanas_sadala, textvariable=mekletais)
    meklesanas_lauks.pack(side='left', fill='x', expand=True)

    planojumu_sadala = ttk.Frame(lapa)
    planojumu_sadala.pack(fill='both', expand=True)
    planojumu_saraksts = tk.Listbox(planojumu_sadala, activestyle='none', height=15, selectmode="single")
    planojumu_saraksts.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(planojumu_saraksts, orient='vertical', command=planojumu_saraksts.yview)
    scrollbar.pack(side='right', fill='y')
    planojumu_saraksts.config(yscrollcommand=scrollbar.set)

    pogu_sadala = ttk.Frame(lapa)
    pogu_sadala.pack(fill='x', pady=(8,0))
    atvert = ttk.Button(pogu_sadala, text="Atvērt", width=12)
    atsvaidzinat = ttk.Button(pogu_sadala, text="Atsvaidzināt", width=12)
    aizvert = ttk.Button(pogu_sadala, text="Aizvērt", width=12, command=root.destroy)
    atvert.pack(side='left', padx=(0,6))
    atsvaidzinat.pack(side='left', padx=(0,6))
    aizvert.pack(side='right')

    planojumi = []
    def iegut_sarakstu():
        nonlocal planojumi
        planojumi = DM.visiPlanojumi()
        lista = mekletais.get().lower()
        planojumu_saraksts.delete(0, 'end')
        for p in planojumi:
            p = "".join(p.split('.')[:-1:])
            if lista == "" or lista in p.lower():
                planojumu_saraksts.insert('end', p)
    def atvert_izveleto(event=None):
        sel = planojumu_saraksts.curselection()
        if not sel:
            messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies plānojumu.")
            return
        plan = planojumu_saraksts.get(sel[0])
        atvertPlanojumu(plan, root)
    def mainas_teksts(*_):
        iegut_sarakstu()
    planojumu_saraksts.bind('<Double-1>', atvert_izveleto)
    atvert.config(command=atvert_izveleto)
    atsvaidzinat.config(command=iegut_sarakstu)
    mekletais.trace_add('write', mainas_teksts)
    iegut_sarakstu()
    root.mainloop()


