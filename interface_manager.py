import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import database_manager as DM
from classes import *
import re

def atvertPlanojumu(nosaukums, planojumuLapa):
    '''
    Palīgfunkcija grupu skata atvēršanai no plānojumu izvēles skata. Tā ņem kā parametrus atveramā plānojuma nosaukumu un plānojumu izvēles lapas objektu, lai plānojumu izvēles lapu aizvērtu.
    
    :param nosaukums: Nosaukums plānojumam, no kura datnes ielasīs datus un attēlos grupu skatā, string vērtība.
    :param planojumuLapa: Plānojuma izvēles lapas objekts, lai aizvērtu izvēles lapu.
    '''
    planojumuLapa.destroy()
    GrupuSkats(DM.iegutPlanojumu(nosaukums))

def mainiKoeficientus(planojums, atjaunot_grupas):
    '''
    Logs koeficientu mainīšanai ar slīdņiem (0-10).
    Atver jaunu logu, kurā var mainīt grupu vērtēšanas koeficientus.
    Pēc saglabāšanas automātiski pārrēķina visu grupu vērtējumus.
    
    :param planojums: Planojums objekts, kuram mainīt koeficientus
    :param atjaunot_grupas: Callback funkcija, ko izsauc pēc koeficientu saglabāšanas
    '''
    # Paša loga izveide
    koef_logs = tk.Toplevel()
    koef_logs.title("Koeficienti")
    koef_logs.geometry("400x300")
    
    galvena_sadala = ttk.Frame(koef_logs, padding=12)
    galvena_sadala.pack(fill='both', expand=True)
    
    ttk.Label(galvena_sadala, text="Grupu vērtēšanas koeficienti", 
              font=font.Font(size=12, weight="bold")).pack(anchor="w", pady=(0,12))
    
    # Slīdņu koeficientiem pilnie nosaukumi
    slideri = {}
    koef_nosaukumi = {
        "blakusNodarbiba": "Blakus nodarbības koeficients",
        "audzeknuPieejamiba": "Audzēkņu pieejamības koeficients",
        "kursaNeesamiba": "Kursa neesamības koeficients",
        "opcijuNeesamiba": "Opciju neesamības koeficients"
    }
    
    # Katram koeficientam izveidots savs slīdnis
    for koef_atslega, koef_teksts in koef_nosaukumi.items():
        sadala = ttk.Frame(galvena_sadala)
        sadala.pack(fill='x', pady=(0,12))
        
        ttk.Label(sadala, text=koef_teksts, width=30).pack(side='left', anchor='w')
        
        vertiba = tk.DoubleVar(value=planojums.Koeficienti[koef_atslega]) # Lai rādītu pašreizējo vērtību
        slideris = ttk.Scale(sadala, from_=0, to=10, orient='horizontal', variable=vertiba)
        slideris.pack(side='left', fill='x', expand=True, padx=(8,8))
        
        vertibas_teksts = ttk.Label(sadala, text=f"{vertiba.get():.1f}", width=4) # Lai redzētu kāda ir uztītā vērtība
        vertibas_teksts.pack(side='left')
        
        # Funkcija, kas atjaunina tekstu, kad slīdnis tiek mainīts
        def atjaunot_tekstu(v, teksts=vertibas_teksts, vert=vertiba):
            teksts.config(text=f"{vert.get():.1f}") # Teksta atjaunināšanai un formatēšanai
        
        slideris.config(command=atjaunot_tekstu)
        slideri[koef_atslega] = vertiba
    
    def saglabat_koef():
        '''Funkcija, kas saglabā jaunos koeficientus un pārrēķina grupu vērtējumus'''
        # Izveidot vārdnīcu ar jaunajiem koeficientiem
        jauni_koef = {atslega: vert.get() for atslega, vert in slideri.items()}
        # Izsaukt plānojuma metodi, kas mainīs koeficientus un pārrēķinās vērtējumus
        planojums.mainitKoeficientus(jauni_koef)
        # Saglabāt plānojumu datnē
        DM.saglabatPlanojumu(planojums)
        # Atjaunot grupu sarakstu interfeisā
        atjaunot_grupas()
        koef_logs.destroy()
    
    def atcelt():
        '''Funkcija, kas aizver logu bez saglabāšanas'''
        koef_logs.destroy()
    
    # Pogas saglabāšanai un atcelšanai
    pogu_sadala = ttk.Frame(galvena_sadala)
    pogu_sadala.pack(fill='x', pady=(12,0))
    ttk.Button(pogu_sadala, text="Saglabāt", command=saglabat_koef).pack(side='left', padx=(0,6))
    ttk.Button(pogu_sadala, text="Atcelt", command=atcelt).pack(side='left')
    
    koef_logs.transient() # lai padarītu logu modālu
    koef_logs.grab_set() # lai nevarētu darboties ar grupām, kamēr koeficientu logs atvērts

def GrupuSkats(planojums):
    '''
    Galvenais grupu skata logs. Attēlo plānojuma grupas un audzēkņus ar filtrēšanas iespējām.
    Lietotājs var skatīt potenciālās/komplektētās grupas vai audzēkņus (komplektētos/nekomplektētos).
    
    :param planojums: Planojums objekts, kuru attēlot
    '''
    # Paša loga izveide
    root = tk.Tk()
    root.title("Grupas — " + planojums.Nosaukums)
    root.geometry("1400x900")
    galvena = ttk.Frame(root, padding=12)
    galvena.pack(fill='both', expand=True)

    nedelas_logs = None
    nedelas_atjaunot = lambda: None

    def atvert_nedelas_skat():
        '''Atver atsevišķu nedēļas skatu ar komplektēto grupu aizpildījumu'''
        nonlocal nedelas_logs, nedelas_atjaunot
        if nedelas_logs is not None and nedelas_logs.winfo_exists():
            nedelas_logs.lift()
            nedelas_atjaunot()
            return

        nedelas_logs = tk.Toplevel(root)
        nedelas_logs.title(f"Nedēļas skats — {planojums.Nosaukums}")
        nedelas_logs.geometry("900x700")

        pamat = ttk.Frame(nedelas_logs, padding=12)
        pamat.pack(fill='both', expand=True)

        ttk.Label(pamat, text="Komplektētās grupas pa laikiem", font=font.Font(size=14, weight="bold")).pack(anchor='w', pady=(0,10))

        fil_krasa = {
            "C": "#4da3ff",
            "A": "#66c266",
            "T": "#ffd966",
            "O": "#c9b3ff",
        }
        fil_kartiba = [
            "Centra (Dagdas iela 4)",
            "Āgenskalna (Kalnciema iela 7A)",
            "Teikas (Zemgaļu iela 8)",
            "Tiešsaistes nodarbības"
        ]

        laiki_no_plana = sorted({g.Laiks for g in planojums.Grupas.values()})

        tabula = ttk.Frame(pamat)
        tabula.pack(fill='both', expand=True)
        tabula.grid_columnconfigure(0, weight=1, minsize=230)

        ttk.Label(tabula, text="Laiks", width=20, font=font.Font(weight="bold")).grid(row=0, column=0, padx=(0,6), sticky='w')
        for ci, fil in enumerate(fil_kartiba, start=1):
            ttk.Label(tabula, text=fil.split('(')[0].strip(), width=12, font=font.Font(weight="bold")).grid(row=0, column=ci, padx=4)

        kvadrati = {}
        current_row = 1
        ieprieks_diena = None
        for laiks_idx in laiki_no_plana:
            diena, _ = laikaIndeksaTulkotajs(laiks_idx)
            if ieprieks_diena is not None and diena != ieprieks_diena:
                tabula.grid_rowconfigure(current_row, minsize=10)
                current_row += 1
            ttk.Label(tabula, text=stringLaiks(laiks_idx), width=28).grid(row=current_row, column=0, sticky='w', padx=(0,6), pady=2)
            for ci, fil in enumerate(fil_kartiba, start=1):
                kv = tk.Label(tabula, width=8, bg='lightgray', relief='solid', bd=1)
                kv.grid(row=current_row, column=ci, padx=4, pady=2, sticky='we')
                kvadrati[(laiks_idx, fil)] = kv
            ieprieks_diena = diena
            current_row += 1

        def atjaunot():
            # Pelēki lauciņi pēc noklusējuma
            for kv in kvadrati.values():
                kv.config(bg='lightgray')

            fil_pilnie = {filialesBurts(nos): nos for nos in fil_kartiba}

            for g in planojums.Grupas.values():
                if not g.Komplekteta:
                    continue
                fil_burts = filialesBurts(g.Filiale)
                krasa = fil_krasa.get(fil_burts, 'lightgray')
                fil_atrasts = fil_pilnie.get(fil_burts, g.Filiale)
                key = (g.Laiks, fil_atrasts)
                if key in kvadrati:
                    kvadrati[key].config(bg=krasa)

        nedelas_atjaunot = atjaunot
        atjaunot()

        def aizvert():
            nonlocal nedelas_logs, nedelas_atjaunot
            nedelas_logs.destroy()
            nedelas_logs = None
            nedelas_atjaunot = lambda: None

        nedelas_logs.protocol("WM_DELETE_WINDOW", aizvert)
    
    def eksportet_planojumu():
        '''Eksportē plānojuma datus lietotājam draudzīgā formātā'''
        # Piedāvāt saglabāšanas vietu un nosaukumu
        datnes_cels = filedialog.asksaveasfilename(
            title="Saglabāt plānojuma eksportu",
            defaultextension=".txt",
            initialfile=f"{planojums.Nosaukums}.txt",
            filetypes=[("Teksta faili", "*.txt"), ("Visi faili", "*.*")]
        )
        
        if not datnes_cels:
            return
        
        try:
            with open(datnes_cels, 'w', encoding='utf-8') as f:
                # Virsraksts
                f.write("=" * 80 + "\n")
                f.write(f"PLĀNOJUMS: {planojums.Nosaukums}\n")
                f.write("=" * 80 + "\n\n")
                
                # Komplektētās grupas
                komplektetas = [g for g in planojums.Grupas.values() if g.Komplekteta]
                komplektetas.sort(key=lambda x: (x.Laiks, x.Filiale, x.Kurss))
                
                f.write(f"KOMPLEKTĒTĀS GRUPAS ({len(komplektetas)})\n")
                f.write("-" * 80 + "\n\n")
                
                if komplektetas:
                    for g in komplektetas:
                        f.write(f"Kods: {g.Kods}\n")
                        f.write(f"Laiks: {stringLaiks(g.Laiks)}\n")
                        f.write(f"Filiāle: {g.Filiale}\n")
                        f.write(f"Kurss: {g.Kurss}\n")
                        f.write(f"Audzekņu skaits: {len(g.Audzekni)}\n")
                        f.write(f"Vērtējums: {g.Vertejums}\n")
                        f.write("\nAudzēkņi:\n")
                        for a in sorted(g.Audzekni, key=lambda x: x.Vards):
                            f.write(f"  • {a.Vards} ({a.PersKods})\n")
                            f.write(f"    Tālrunis: {a.TelNr}, E-pasts: {a.Epasts}\n")
                        f.write("\n" + "-" * 80 + "\n\n")
                else:
                    f.write("Nav komplektētu grupu.\n\n")
                
                # Potenciālās grupas
                potencialas = [g for g in planojums.Grupas.values() if not g.Komplekteta and len(g.Audzekni) > 0]
                potencialas.sort(key=lambda x: x.Vertejums, reverse=True)
                
                f.write(f"\nPOTENCIĀLĀS GRUPAS ({len(potencialas)})\n")
                f.write("-" * 80 + "\n\n")
                
                if potencialas:
                    for g in potencialas[:20]:  # Tikai top 20
                        f.write(f"Kods: {g.Kods} | Vērtējums: {g.Vertejums}\n")
                        f.write(f"Laiks: {stringLaiks(g.Laiks)} | Filiāle: {g.Filiale}\n")
                        f.write(f"Kurss: {g.Kurss} | Audzekņi: {len(g.Audzekni)}\n")
                        f.write("\n")
                    if len(potencialas) > 20:
                        f.write(f"... un vēl {len(potencialas) - 20} potenciālās grupas\n\n")
                else:
                    f.write("Nav potenciālu grupu.\n\n")
                
                # Audzēkņu kopsavilkums
                visi_audzekni = list(planojums.Audzekni.values())
                komplekteti_audz = [a for a in visi_audzekni if a.Komplektets]
                nekomplekteti_audz = [a for a in visi_audzekni if not a.Komplektets]
                
                f.write(f"\nAUDZĒKŅU KOPSAVILKUMS\n")
                f.write("-" * 80 + "\n\n")
                f.write(f"Kopā audzēkņi: {len(visi_audzekni)}\n")
                f.write(f"Komplektēti: {len(komplekteti_audz)}\n")
                f.write(f"Nekomplektēti: {len(nekomplekteti_audz)}\n\n")
                
                if nekomplekteti_audz:
                    f.write("Nekomplektētie audzēkņi:\n")
                    for a in sorted(nekomplekteti_audz, key=lambda x: x.Vards):
                        f.write(f"  • {a.Vards} ({a.PersKods})\n")
                        f.write(f"    Kursi: {', '.join(a.Kursi)}\n")
                        f.write(f"    Filiāles: {', '.join(a.Filiales)}\n")
                        f.write(f"    Kontakti: {a.TelNr}, {a.Epasts}\n\n")
                
                f.write("\n" + "=" * 80 + "\n")
            
            messagebox.showinfo("Izdevās", f"Plānojums veiksmīgi eksportēts uz:\n{datnes_cels}")
        
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās eksportēt plānojumu:\n{str(e)}")
    
    # *************** Galvene ****************
    galvenes_sadala = ttk.Frame(galvena)
    galvenes_sadala.pack(fill='x', anchor="w", pady=(0,8))
    
    galvenes_fonts = font.Font(size=16, weight="bold")
    ttk.Label(galvenes_sadala, text="Plānojums: " + planojums.Nosaukums, font=galvenes_fonts).pack(side='left')
    
    # Pogas labajā pusē
    pogu_galvene = ttk.Frame(galvenes_sadala)
    pogu_galvene.pack(side='right', padx=(8,0))
    ttk.Button(pogu_galvene, text="Pievienot audzēkni",
               command=lambda: pievienot_audzekni()).pack(side='left', padx=(0,6))
    ttk.Button(pogu_galvene, text="Nedēļa",
               command=atvert_nedelas_skat).pack(side='left', padx=(0,6))
    ttk.Button(pogu_galvene, text="Eksportēt",
               command=eksportet_planojumu).pack(side='left', padx=(0,6))
    ttk.Button(pogu_galvene, text="Koeficienti", 
               command=lambda: mainiKoeficientus(planojums, ieladet_grupas)).pack(side='left', padx=(0,6))
    ttk.Button(pogu_galvene, text="Mainīt plānojumu", 
               command=lambda: [root.destroy(), PlanojumuSkats()]).pack(side='left', padx=(0,6))
    ttk.Button(pogu_galvene, text="Aizvērt", command=root.destroy).pack(side='left')

    # ************* Filtri ****************
    filtru_sadala = ttk.LabelFrame(galvena, text="Filtri", padding=10)
    filtru_sadala.pack(fill='x', pady=(8,0))

    # Savākt unikālās vērtības no plānojuma grupām
    filialu_kopa = set()
    kursu_kopa = set()
    laiku_kopa = set()
    for g in planojums.Grupas.values():
        filialu_kopa.add(g.Filiale)
        kursu_kopa.add(g.Kurss)
        laiku_kopa.add(g.Laiks)
    
    filiales = sorted(list(filialu_kopa))
    kursi = sorted(list(kursu_kopa))
    laiki = sorted(list(laiku_kopa))

    # Filtra mainīgie
    izveleta_filiale = tk.StringVar(value="Visi")
    izveletais_kurss = tk.StringVar(value="Visi")
    izveletie_laiki = set()  # Kopa ar izvēlētajiem laiku indeksiem

    # ******** Filiāļu filtrs *********
    fil_konteiners = ttk.Frame(filtru_sadala)
    fil_konteiners.grid(row=0, column=0, sticky='nw', padx=(0,20))
    ttk.Label(fil_konteiners, text="Filiāle:", font=font.Font(weight="bold")).pack(anchor='w', pady=(0,4))
    fil_sadala = ttk.Frame(fil_konteiners)
    fil_sadala.pack(anchor='w')
    ttk.Radiobutton(fil_sadala, text="Visi", variable=izveleta_filiale, value="Visi").pack(anchor='w', pady=1)
    for fil in filiales:
        # Īss nosaukums, ja filiāle ir pārāk gara
        fil_iss = fil.split('(')[0].strip() if '(' in fil else fil[:20]
        ttk.Radiobutton(fil_sadala, text=fil_iss, variable=izveleta_filiale, value=fil).pack(anchor='w', pady=1)

    # ******** Kursu filtrs *********
    kursa_konteiners = ttk.Frame(filtru_sadala)
    kursa_konteiners.grid(row=0, column=1, sticky='nw', padx=(0,20))
    ttk.Label(kursa_konteiners, text="Kurss:", font=font.Font(weight="bold")).pack(anchor='w', pady=(0,4))
    kursa_izvelne = ttk.Combobox(kursa_konteiners, textvariable=izveletais_kurss, state='readonly', width=35)
    kursa_izvelne['values'] = ["Visi"] + kursi
    kursa_izvelne.pack(anchor='w')

    # ******** Laiku filtrs *********
    laika_konteiners = ttk.Frame(filtru_sadala)
    laika_konteiners.grid(row=0, column=2, sticky='nw')
    ttk.Label(laika_konteiners, text="Laiki:", font=font.Font(weight="bold")).pack(anchor='w', pady=(0,4))
    
    laika_rezgis = ttk.Frame(laika_konteiners)
    laika_rezgis.pack(anchor='w')
    
    dienas = ["Pirm", "Otr", "Treš", "Ceturt", "Piekt", "Sest"]
    darba_laiki = ["16:00", "17:30", "19:00"]
    sestd_laiki = ["10:00", "11:30", "13:00", "15:00", "16:30", "18:00"]
    
    laiku_pogas = {}  # Saglabā references uz laiku pogām
    
    # "Visi" laiki atzīmējamais lauciņš
    visi_laiki_main = tk.BooleanVar(value=True)
    def parslegt_visus():
        '''Pārslēdz visus laikus (ieslēdz vai izslēdz)'''
        if visi_laiki_main.get():
            izveletie_laiki.clear()
            for pogas_dati in laiku_pogas.values():
                pogas_dati[1].config(relief='raised', bg='SystemButtonFace')
        ieladet_grupas()
    
    visu_poga = ttk.Checkbutton(laika_rezgis, text="Visi", variable=visi_laiki_main, command=parslegt_visus)
    visu_poga.grid(row=0, column=0, columnspan=7, sticky='w', pady=(0,4))
    
    def laika_klikskis(laika_indekss, poga):
        '''Apstrādā laika pogas klikšķi - pārslēdz izvēlēto laiku'''
        visi_laiki_main.set(False)  # Noņemt "Visi" atzīmi
        if laika_indekss in izveletie_laiki:
            # Ja laiks jau ir izvēlēts, noņem to
            izveletie_laiki.remove(laika_indekss)
            poga.config(relief='raised', bg='SystemButtonFace')
        else:
            # Ja laiks nav izvēlēts, pievieno to
            izveletie_laiki.add(laika_indekss)
            poga.config(relief='sunken', bg='lightblue')
        ieladet_grupas()  # Atjaunot grupu sarakstu
    
    # Izveidot laiku pogu režģi
    for diena_idx, diena in enumerate(dienas):
        ttk.Label(laika_rezgis, text=diena, font=font.Font(weight="bold"), width=8).grid(row=diena_idx+2, column=0, sticky='w', padx=(0,4))
        
        if diena_idx < 5:
            # Darba dienas (3 laiki)
            for laiks_idx in range(3):
                laika_indekss = diena_idx * 3 + laiks_idx
                if laika_indekss in laiku_kopa:
                    poga = tk.Button(laika_rezgis, text=darba_laiki[laiks_idx], width=6, relief='raised',
                                  command=lambda li=laika_indekss, b=None: laika_klikskis(li, laiku_pogas[li][1]))
                    poga.grid(row=diena_idx+2, column=laiks_idx+1, padx=2, pady=2)
                    laiku_pogas[laika_indekss] = (laika_indekss, poga)
        else:
            # Sestdiena (6 laiki)
            for laiks_idx in range(6):
                laika_indekss = 15 + laiks_idx
                if laika_indekss in laiku_kopa:
                    poga = tk.Button(laika_rezgis, text=sestd_laiki[laiks_idx], width=6, relief='raised',
                                  command=lambda li=laika_indekss, b=None: laika_klikskis(li, laiku_pogas[li][1]))
                    poga.grid(row=diena_idx+2, column=laiks_idx+1, padx=2, pady=2)
                    laiku_pogas[laika_indekss] = (laika_indekss, poga)

    # # ******** Galvenais saturs *********
    satura_sadala = ttk.Frame(galvena)
    satura_sadala.pack(fill='both', expand=True, pady=8)

    # # ******** Grupas un audzēkņu dati *********
    kreisa_puse = ttk.Frame(satura_sadala)
    kreisa_puse.pack(side='left', fill='both', expand=True, padx=(0,12))
    
    # Saraksta galvene ar skaitu
    saraksta_galvene = ttk.Frame(kreisa_puse)
    saraksta_galvene.pack(fill='x')
    ttk.Label(saraksta_galvene, text="Grupas", font=font.Font(weight="bold")).pack(side='left')
    skaita_teksts = ttk.Label(saraksta_galvene, text="(0)", foreground='gray')
    skaita_teksts.pack(side='left', padx=(4,0))

    # ******** Saraksta satura filtri *********
    satura_veida_sadala = ttk.Frame(kreisa_puse)
    satura_veida_sadala.pack(fill='x', pady=(4,4))
    
    satura_veids = tk.StringVar(value="grupas")
    ttk.Radiobutton(satura_veida_sadala, text="Grupas", variable=satura_veids, 
                    value="grupas", command=lambda: [radit_veida_opcijas(), ieladet_grupas()]).pack(side='left', padx=(0,12))
    ttk.Radiobutton(satura_veida_sadala, text="Audzēkņi", variable=satura_veids, 
                    value="audzekni", command=lambda: [radit_veida_opcijas(), ieladet_grupas()]).pack(side='left')
    
    veida_opciju_sadala = ttk.Frame(kreisa_puse)
    veida_opciju_sadala.pack(fill='x', pady=(2,4))
    
    # Grupu veida opcijas
    grupas_veids = tk.StringVar(value="potencialas")
    grupas_poga1 = ttk.Radiobutton(veida_opciju_sadala, text="Potenciālās", variable=grupas_veids, 
                    value="potencialas", command=lambda: ieladet_grupas())
    grupas_poga2 = ttk.Radiobutton(veida_opciju_sadala, text="Komplektētās", variable=grupas_veids, 
                    value="komplektetas", command=lambda: ieladet_grupas())
    
    # Audzēkņu veida opcijas
    audzeknu_veids = tk.StringVar(value="nekomplekteti")
    audzeknu_poga1 = ttk.Radiobutton(veida_opciju_sadala, text="Nekomplektētie", variable=audzeknu_veids, 
                    value="nekomplekteti", command=lambda: ieladet_grupas())
    audzeknu_poga2 = ttk.Radiobutton(veida_opciju_sadala, text="Komplektētie", variable=audzeknu_veids, 
                    value="komplekteti", command=lambda: ieladet_grupas())
    
    def radit_veida_opcijas():
        '''Parāda atbilstošās apakšopcijas atkarībā vai izvēlētas grupas vai audzēkņi'''
        # Paslēpt visas pogas
        for widgets in veida_opciju_sadala.winfo_children():
            widgets.pack_forget()
        
        # Parādīt atbilstošās pogas
        if satura_veids.get() == "grupas":
            grupas_poga1.pack(side='left', padx=(0,12))
            grupas_poga2.pack(side='left')
        else:
            audzeknu_poga1.pack(side='left', padx=(0,12))
            audzeknu_poga2.pack(side='left')
    
    radit_veida_opcijas()
    
    # ******** Saraksts *********
    saraksta_sadala = ttk.Frame(kreisa_puse)
    saraksta_sadala.pack(fill='both', expand=True)
    
    saraksta_logs = tk.Listbox(saraksta_sadala, activestyle='none', width=60)
    saraksta_logs.pack(side='left', fill='both', expand=True)
    ritjosla = ttk.Scrollbar(saraksta_sadala, orient='vertical', command=saraksta_logs.yview)
    ritjosla.pack(side='right', fill='y')
    saraksta_logs.config(yscrollcommand=ritjosla.set)

    ttk.Separator(kreisa_puse, orient='horizontal').pack(fill='x', pady=(8,8))
    
    # ******** Audzēkņa dati *********
    audzekna_detalu_sadala = ttk.LabelFrame(kreisa_puse, text="Audzeknis", padding=6)
    audzekna_detalu_sadala.pack(fill='x')
    
    # Izvietojums: informācija kreisajā kolonnā, pieejamības režģis labajā
    aud_info_bloks = ttk.Frame(audzekna_detalu_sadala)
    aud_info_bloks.pack(fill='x', expand=True)
    info_kolone = ttk.Frame(aud_info_bloks)
    info_kolone.pack(side='left', anchor='nw', padx=(0,8))

    # Izveidot teksta laukus audzēkņa informācijai
    aud_teksts_vards = ttk.Label(info_kolone, text="Vārds: —", font=font.Font(weight="bold"))
    aud_teksts_perspk = ttk.Label(info_kolone, text="Personas kods: —", font=font.Font(size=9))
    aud_teksts_talr = ttk.Label(info_kolone, text="Tālrunis: —", font=font.Font(size=9))
    aud_teksts_epasts = ttk.Label(info_kolone, text="E-pasts: —", font=font.Font(size=9))
    aud_teksts_filiales = ttk.Label(info_kolone, text="Filiāles: —", font=font.Font(size=9))
    aud_teksts_kursi = ttk.Label(info_kolone, text="Kursi: —", font=font.Font(size=9))
    aud_teksts_pieejamiba = ttk.Label(info_kolone, text="Pieejamība: —", font=font.Font(size=9))
    
    aud_teksts_vards.pack(anchor="w", pady=(0,2))
    aud_teksts_perspk.pack(anchor="w", pady=(0,1))
    aud_teksts_talr.pack(anchor="w", pady=(0,1))
    aud_teksts_epasts.pack(anchor="w", pady=(0,1))
    aud_teksts_filiales.pack(anchor="w", pady=(0,1))
    aud_teksts_kursi.pack(anchor="w", pady=(0,1))
    aud_teksts_pieejamiba.pack(anchor="w", pady=(0,0))

    # Pieejamības vizuālais režģis (zaļš = var, pelēks = nevar)
    aud_pieejamiba_rezgis = ttk.Frame(aud_info_bloks)
    aud_pieejamiba_rezgis.pack(side='left', anchor='nw', pady=(0,0), fill='both', expand=True)

    # Audzēkņa darbību pogas
    aud_pogas = ttk.Frame(aud_info_bloks)
    aud_pogas.pack(side='left', anchor='ne', padx=(8,0))
    dzest_audzekni_poga = ttk.Button(aud_pogas, text="Dzēst audzēkni")
    dzest_audzekni_poga.pack(anchor='n')

    def notirit_pieejamibas_rezginju():
        '''Notīra pieejamības režģi'''
        for w in aud_pieejamiba_rezgis.winfo_children():
            w.destroy()

    # ******** Grupas dati *********
    laba_puse = ttk.Frame(satura_sadala)
    laba_puse.pack(side='left', fill='both', expand=True)

    detalu_virsraksts = ttk.Label(laba_puse, text="Izvēlies grupu", font=font.Font(size=14, weight="bold"))
    detalu_virsraksts.pack(anchor="w")
    
    detalu_sadala = ttk.Frame(laba_puse, padding=6)
    detalu_sadala.pack(fill='both', expand=True, pady=(6,0))

    # Grupas informācijas lauki
    teksts_kods = ttk.Label(detalu_sadala, text="Kods: —")
    teksts_laiks = ttk.Label(detalu_sadala, text="Laiks: —")
    teksts_filiale = ttk.Label(detalu_sadala, text="Filiāle: —")
    teksts_kurss = ttk.Label(detalu_sadala, text="Kurss: —")
    teksts_skaits = ttk.Label(detalu_sadala, text="Audzekņu skaits: —")
    teksts_vertejums = ttk.Label(detalu_sadala, text="Vērtējums: —", font=font.Font(size=11, weight="bold"))
    
    teksts_kods.pack(anchor="w", pady=(0,4))
    teksts_laiks.pack(anchor="w", pady=(0,4))
    teksts_filiale.pack(anchor="w", pady=(0,4))
    teksts_kurss.pack(anchor="w", pady=(0,4))
    teksts_skaits.pack(anchor="w", pady=(0,4))
    teksts_vertejums.pack(anchor="w", pady=(0,8))
    
    # ******** Komplektēšanas poga *********
    def komplektet_grupu():
        '''Komplektē izvēlēto grupu pēc apstiprinājuma'''
        if pasreizeja_grupa and not pasreizeja_grupa.Komplekteta:
            atbilde = messagebox.askyesno(
                "Komplektēt grupu",
                f"Vai tiešām vēlaties komplektēt grupu {pasreizeja_grupa.Kods}?\n\n"
                f"Audzekņu skaits: {len(pasreizeja_grupa.Audzekni)}\n"
                f"Laiks: {stringLaiks(pasreizeja_grupa.Laiks)}\n"
                f"Filiāle: {pasreizeja_grupa.Filiale}\n"
                f"Kurss: {pasreizeja_grupa.Kurss}"
            )
            if atbilde:
                # Izsaukt plānojuma metodi grupas komplektēšanai
                planojums.komplektetGrupu(pasreizeja_grupa.Kods)
                DM.saglabatPlanojumu(planojums)
                notirit_detalas()
                ieladet_grupas()
                messagebox.showinfo("Izdevās", f"Grupa {pasreizeja_grupa.Kods} ir veiksmīgi komplektēta!")
        elif pasreizeja_grupa and pasreizeja_grupa.Komplekteta:
            messagebox.showinfo("Grupa jau komplektēta", "Šī grupa jau ir komplektēta.")
    
    def atkomplektet_grupu():
        '''Atkomplektē izvēlēto grupu pēc apstiprinājuma'''
        if pasreizeja_grupa and pasreizeja_grupa.Komplekteta:
            atbilde = messagebox.askyesno(
                "Atkomplektēt grupu",
                f"Vai tiešām vēlaties atkomplektēt grupu {pasreizeja_grupa.Kods}?\n\n"
                f"Audzekņu skaits: {len(pasreizeja_grupa.Audzekni)}\n"
                f"Laiks: {stringLaiks(pasreizeja_grupa.Laiks)}\n"
                f"Filiāle: {pasreizeja_grupa.Filiale}\n"
                f"Kurss: {pasreizeja_grupa.Kurss}\n\n"
                f"Visi grupas audzēkņi tiks atzīmēti kā nekomplektēti un atgriezīsies potenciālajās grupās."
            )
            if atbilde:
                # Izsaukt plānojuma metodi grupas atkomplektēšanai
                if planojums.atkomplektetGrupu(pasreizeja_grupa.Kods):
                    DM.saglabatPlanojumu(planojums)
                    notirit_detalas()
                    ieladet_grupas()
                    messagebox.showinfo("Izdevās", f"Grupa {pasreizeja_grupa.Kods} ir veiksmīgi atkomplektēta!")
                else:
                    messagebox.showerror("Kļūda", "Neizdevās atkomplektēt grupu.")
        elif pasreizeja_grupa and not pasreizeja_grupa.Komplekteta:
            messagebox.showinfo("Grupa nav komplektēta", "Šī grupa nav komplektēta, tāpēc to nevar atkomplektēt.")

    pogu_ramis = ttk.Frame(detalu_sadala)
    pogu_ramis.pack(anchor="w", pady=(0,8))
    komplektesanas_poga = ttk.Button(pogu_ramis, text="Komplektēt grupu", command=komplektet_grupu)
    komplektesanas_poga.pack(side='left', padx=(0,6))
    atkomplektesanas_poga = ttk.Button(pogu_ramis, text="Atkomplektēt", command=atkomplektet_grupu)
    atkomplektesanas_poga.pack(side='left')

    ttk.Separator(detalu_sadala, orient='horizontal').pack(fill='x', pady=(4,8))
    ttk.Label(detalu_sadala, text="Audzekņi grupā:", font=font.Font(weight="bold")).pack(anchor="w", pady=(0,4))
    
    # ******** Audzēkņu saraksts grupā *********
    audzeknu_konteiners = ttk.Frame(detalu_sadala)
    audzeknu_konteiners.pack(fill='both', expand=True)
    
    audzeknu_saraksts = tk.Listbox(audzeknu_konteiners, width=60, activestyle='none')
    audzeknu_saraksts.pack(side='left', fill='both', expand=True)
    audzeknu_ritjosla = ttk.Scrollbar(audzeknu_konteiners, orient='vertical', command=audzeknu_saraksts.yview)
    audzeknu_ritjosla.pack(side='right', fill='y')
    audzeknu_saraksts.config(yscrollcommand=audzeknu_ritjosla.set)

    # ******** GLOBĀLIE MAINĪGIE ********
    saraksts = []  # Filtrēto grupu/audzēkņu saraksts
    pasreizeja_grupa = None  # Pašreiz izvēlētā grupa
    pasreizejais_audzeknis = None  # Pašreiz izvēlētais audzēknis
    audzeknu_rindu_karte = {}  # Kartē teksta rindu numuru uz audzēkni

    def ieladet_grupas():
        '''
        Ielādē un filtrē grupas vai audzēkņus atkarībā no izvēlētajiem filtriem.
        Atjauno saraksta logu ar filtrētajiem rezultātiem.
        '''
        nonlocal saraksts
        veids = satura_veids.get()
        
        if veids == "audzekni":
            # ******** Audzēkņu režīms *********
            komplekteto_stavoklis = audzeknu_veids.get()
            visi_audzekni = list(planojums.Audzekni.values()) if isinstance(planojums.Audzekni, dict) else list(planojums.Audzekni)
            
            fil_vert = izveleta_filiale.get()
            kursa_vert = izveletais_kurss.get()
            
            filtreti = []
            for a in visi_audzekni:
                # Filtrēt pēc komplektēšanas statusa
                if komplekteto_stavoklis == "nekomplekteti" and a.Komplektets:
                    continue
                if komplekteto_stavoklis == "komplekteti" and not a.Komplektets:
                    continue
                
                # Filiāles filtrs
                if fil_vert != "Visi" and fil_vert not in a.Filiales:
                    continue
                
                # Kursu filtrs
                if kursa_vert != "Visi" and kursa_vert not in a.Kursi:
                    continue
                
                # Laiku filtrs
                if not visi_laiki_main.get() and len(izveletie_laiki) > 0:
                    pieejams = False
                    for laiks_idx in izveletie_laiki:
                        if a.laiksPieejams(laiks_idx):
                            pieejams = True
                            break
                    if not pieejams:
                        continue
                
                filtreti.append(a)
            
            # Kārtot alfabētiski pēc vārda
            saraksts = sorted(filtreti, key=lambda x: x.Vards)
            
            # Atjaunot saraksta logu
            saraksta_logs.delete(0, 'end')
            for a in saraksts:
                saraksta_logs.insert('end', a.Vards)
            
            skaita_teksts.config(text=f"({len(saraksts)})")
            notirit_detalas()
            
        else:
            # ******** Grupu režīms *********
            visas_grupas = list(planojums.Grupas.values()) if isinstance(planojums.Grupas, dict) else list(planojums.Grupas)
            
            fil_vert = izveleta_filiale.get()
            kursa_vert = izveletais_kurss.get()
            grupas_stavoklis = grupas_veids.get()
            
            # Iegūt visas komplektētās grupas laiku/filiāļu kombinācijas
            # (lai izslēgtu potenciālās grupas ar tādu pašu laiku/filiāli)
            komplekteto_sloti = set()
            for g in visas_grupas:
                if g.Komplekteta:
                    komplekteto_sloti.add((g.Laiks, g.Filiale))
            filtreti = []
            for g in visas_grupas:
                # Filtrēt pēc grupas statusa (potenciālā vai komplektētā)
                if grupas_stavoklis == "potencialas":
                    # Izslēgt komplektētās grupas un grupas ar to pašu laiku/filiāli kā komplektētajām
                    if g.Komplekteta or (g.Laiks, g.Filiale) in komplekteto_sloti:
                        continue
                else:  # komplektētas
                    # Rādīt tikai komplektētās
                    if not g.Komplekteta:
                        continue
                
                # Pārējie filtri
                if fil_vert != "Visi" and g.Filiale != fil_vert:
                    continue
                if kursa_vert != "Visi" and g.Kurss != kursa_vert:
                    continue
                if not visi_laiki_main.get() and len(izveletie_laiki) > 0:
                    if g.Laiks not in izveletie_laiki:
                        continue
                filtreti.append(g)
            
            # Kārtot atkarībā no statusa
            if grupas_stavoklis == "potencialas":
                # Potenciālās grupas kārtot pēc vērtējuma (augstākais pirmais)
                saraksts = sorted(filtreti, key=lambda x: x.Vertejums, reverse=True)
            else:
                # Komplektētās grupas kārtot pēc koda
                saraksts = sorted(filtreti, key=lambda x: x.Kods)
            
            # Atjaunot saraksta logu
            saraksta_logs.delete(0, 'end')
            for g in saraksts:
                if grupas_stavoklis == "potencialas":
                    teksts = f"{g.Kods} — Vērtējums: {g.Vertejums}"
                else:
                    teksts = g.Kods
                saraksta_logs.insert('end', teksts)
            
            skaita_teksts.config(text=f"({len(saraksts)})")
            notirit_detalas()

        nedelas_atjaunot()

    def notirit_detalas():
        '''Notīra visus detaļu laukus (gan grupas, gan audzēkņa informāciju)'''
        detalu_virsraksts.config(text="Izvēlies grupu")
        teksts_kods.config(text="Kods: —")
        teksts_laiks.config(text="Laiks: —")
        teksts_filiale.config(text="Filiāle: —")
        teksts_kurss.config(text="Kurss: —")
        teksts_skaits.config(text="Audzekņu skaits: —")
        teksts_vertejums.config(text="Vērtējums: —")
        audzeknu_saraksts.delete(0, 'end')

        
        notirit_audzekna_detalas()

    def notirit_audzekna_detalas():
        '''Notīra audzēkņa detaļu laukus'''
        aud_teksts_vards.config(text="Vārds: —")
        aud_teksts_perspk.config(text="Personas kods: —")
        aud_teksts_talr.config(text="Tālrunis: —")
        aud_teksts_epasts.config(text="E-pasts: —")
        aud_teksts_filiales.config(text="Filiāles: —")
        aud_teksts_kursi.config(text="Kursi: —")
        aud_teksts_pieejamiba.config(text="Pieejamība: —")
        notirit_pieejamibas_rezginju()
        dzest_audzekni_poga.state(['disabled'])

    def pievienot_audzekni():
        '''Atver modālu logu jauna audzēkņa pievienošanai'''
        logs = tk.Toplevel(root)
        logs.title("Pievienot audzēkni")
        logs.geometry("900x920")
        logs.transient(root)
        logs.grab_set()

        pamat = ttk.Frame(logs, padding=12)
        pamat.pack(fill='both', expand=True)

        lauki = ttk.Frame(pamat)
        lauki.pack(fill='x', pady=(0,10))
        vards_var = tk.StringVar()
        persk_var = tk.StringVar()
        talr_var = tk.StringVar()
        epasts_var = tk.StringVar()

        def ievades_rinda(rinda, teksts, var, plat=40):
            ttk.Label(lauki, text=teksts, width=18).grid(row=rinda, column=0, sticky='w', pady=2)
            ttk.Entry(lauki, textvariable=var, width=plat).grid(row=rinda, column=1, sticky='w', pady=2)
        ievades_rinda(0, "Vārds un uzvārds:", vards_var)
        ievades_rinda(1, "Personas kods:", persk_var)
        ievades_rinda(2, "Tālrunis:", talr_var)
        ievades_rinda(3, "E-pasts:", epasts_var)

        keisi = ttk.Frame(pamat)
        keisi.pack(fill='x', pady=(0,10))
        ttk.Label(keisi, text="Filiāles:", font=font.Font(weight="bold")).grid(row=0, column=0, sticky='w')
        ttk.Label(keisi, text="Kursi:", font=font.Font(weight="bold")).grid(row=0, column=1, sticky='w', padx=(20,0))

        fil_vars = {}
        kurs_vars = {}
        for i, fil in enumerate(Filiales.keys(), start=1):
            fil_vars[fil] = tk.BooleanVar(value=False)
            ttk.Checkbutton(keisi, text=fil, variable=fil_vars[fil]).grid(row=i, column=0, sticky='w', pady=1)
        for j, kurss in enumerate(Kursi.keys(), start=1):
            kurs_vars[kurss] = tk.BooleanVar(value=False)
            ttk.Checkbutton(keisi, text=kurss, variable=kurs_vars[kurss]).grid(row=j, column=1, sticky='w', pady=1, padx=(20,0))

        laiku_sadala = ttk.LabelFrame(pamat, text="Pieejamie laiki (zaļš = var, pelēks = nevar)", padding=8)
        laiku_sadala.pack(fill='x', pady=(0,10))

        laiki_map = jauniLaiki()
        for d in laiki_map:
            for l in laiki_map[d]:
                laiki_map[d][l] = False  # lai sākumā visi būtu atzīmēti kā nepieejami

        dienas_txt = ["Pirm", "Otr", "Treš", "Cet", "Piekt", "Sest"]
        darba_laiki = ["16:00", "17:30", "19:00"]
        sest_laiki = ["10:00", "11:30", "13:00", "15:00", "16:30", "18:00"]

        laika_pogas = {}

        def parsl_laiku(diena, laiks):
            '''Pārslēdz laiku pieejamību un atjaunina pogas krāsu'''
            laiki_map[diena][laiks] = not laiki_map[diena][laiks]
            laika_pogas[(diena, laiks)].config(bg="lightgreen" if laiki_map[diena][laiks] else "lightgray")


        darba_frame = ttk.Frame(laiku_sadala)
        darba_frame.pack(anchor="w", pady=(0,8))
        
        ttk.Label(darba_frame, text="", width=10).grid(row=0, column=0)
        for ci, txt in enumerate(darba_laiki, start=1):
            ttk.Label(darba_frame, text=txt, width=8, font=font.Font(weight="bold")).grid(row=0, column=ci, padx=2)
        
        for di in range(1, 6):
            ttk.Label(darba_frame, text=dienas_txt[di-1], width=10).grid(row=di, column=0, sticky='w')
            for li in range(1, 4):
                btn = tk.Button(darba_frame, width=4, height=1, bg="lightgray", relief='solid', bd=1,
                                 command=lambda d=di, l=li: parsl_laiku(d, l))
                btn.grid(row=di, column=li, padx=2, pady=2)
                laika_pogas[(di, li)] = btn
        
        sest_frame = ttk.Frame(laiku_sadala)
        sest_frame.pack(anchor="w")
        
        ttk.Label(sest_frame, text="", width=10).grid(row=0, column=0)
        for ci, txt in enumerate(sest_laiki, start=1):
            ttk.Label(sest_frame, text=txt, width=8, font=font.Font(weight="bold")).grid(row=0, column=ci, padx=2)
        
        ttk.Label(sest_frame, text=dienas_txt[5], width=10).grid(row=1, column=0, sticky='w')
        for li in range(1, 7):
            btn = tk.Button(sest_frame, width=4, height=1, bg="lightgray", relief='solid', bd=1,
                             command=lambda d=6, l=li: parsl_laiku(d, l))
            btn.grid(row=1, column=li, padx=2, pady=2)
            laika_pogas[(6, li)] = btn

        pogas = ttk.Frame(pamat)
        pogas.pack(fill='x', pady=(6,0))

        def saglabat():
            vards = vards_var.get().strip()
            pers = persk_var.get().strip()
            talr = talr_var.get().strip()
            ep = epasts_var.get().strip()
            fil_sel = [f for f,v in fil_vars.items() if v.get()]
            kur_sel = [k for k,v in kurs_vars.items() if v.get()]
            laiki_izv = any(laiki_map[d][l] for d in laiki_map for l in laiki_map[d])

            if not vards or not pers:
                messagebox.showwarning("Brīdinājums", "Lūdzu, ievadi vārdu un personas kodu.")
                return
            if not fil_sel:
                messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies vismaz vienu filiāli.")
                return
            if not kur_sel:
                messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies vismaz vienu kursu.")
                return
            if not laiki_izv:
                messagebox.showwarning("Brīdinājums", "Lūdzu, atzīmē vismaz vienu pieejamo laiku.")
                return

            laiki_kopa = {}
            for d, laiki in laiki_map.items():
                laiki_kopa[d] = {l: pieej for l, pieej in laiki.items()}

            jaunais = Audzeknis(vards, pers, laiki_kopa, fil_sel, kur_sel, talr, ep)
            planojums.pievienotAudzekniPilns(jaunais)
            DM.saglabatPlanojumu(planojums)
            
            
            ieladet_grupas()
            messagebox.showinfo("Izdevās", f"Audzēknis {vards} pievienots.")
            logs.destroy()

        ttk.Button(pogas, text="Saglabāt", command=saglabat).pack(side='left', padx=(0,8))
        ttk.Button(pogas, text="Atcelt", command=logs.destroy).pack(side='left')

    def dzest_atlasito_audzekni():
        '''Dzēš pašreiz atlasīto audzēkni pēc apstiprinājuma'''
        nonlocal pasreizejais_audzeknis
        if not pasreizejais_audzeknis:
            messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies audzēkni, ko dzēst.")
            return
        a = pasreizejais_audzeknis
        if not messagebox.askyesno("Apstiprinājums", f"Vai tiešām dzēst audzēkni {a.Vards}?\nPersonas kods: {a.PersKods}"):
            return

        if planojums.dzestAudzekni(a.PersKods):
            DM.saglabatPlanojumu(planojums)
            pasreizejais_audzeknis = None
            notirit_detalas()
            ieladet_grupas()
            messagebox.showinfo("Izdevās", "Audzēknis dzēsts.")
        else:
            messagebox.showerror("Kļūda", "Neizdevās atrast audzēkni dzēšanai.")

    def uzzimet_pieejamibu(a):
        '''Zīmē audzēkņa pieejamības režģi ar krāsām (zaļš = var, pelēks = nevar)'''
        notirit_pieejamibas_rezginju()

        ttk.Label(
            aud_pieejamiba_rezgis,
            text="Pieejamība (zaļš = var, pelēks = nevar)",
            font=font.Font(size=9, weight="bold")
        ).pack(anchor="w", pady=(0,4))

        # Darba dienas (1–5) ar 3 laikiem
        darba_frame = ttk.Frame(aud_pieejamiba_rezgis)
        darba_frame.pack(anchor="w", pady=(0,4))
        darba_laiki = ["16:00", "17:30", "19:00"]
        ttk.Label(darba_frame, text="", width=8).grid(row=0, column=0)
        for ci, laiks_txt in enumerate(darba_laiki, start=1):
            ttk.Label(darba_frame, text=laiks_txt, width=6).grid(row=0, column=ci, padx=2)
        dienas_teksts = ["Pirm", "Otr", "Treš", "Cet", "Piekt"]
        for di, diena_txt in enumerate(dienas_teksts):
            ttk.Label(darba_frame, text=diena_txt, width=8).grid(row=di+1, column=0, sticky="w")
            for li in range(3):
                laika_indekss = di * 3 + li
                pieejams = a.laiksPieejams(laika_indekss)
                krasa = "lightgreen" if pieejams else "lightgray"
                tk.Label(
                    darba_frame,
                    bg=krasa,
                    width=3,
                    height=1,
                    relief='solid',
                    bd=1
                ).grid(row=di+1, column=li+1, padx=2, pady=1)

        # Sestdiena ar 6 laikiem
        sest_frame = ttk.Frame(aud_pieejamiba_rezgis)
        sest_frame.pack(anchor="w")
        sest_laiki = ["10:00", "11:30", "13:00", "15:00", "16:30", "18:00"]
        
        for ci, laiks_txt in enumerate(sest_laiki, start=1):
            ttk.Label(sest_frame, text=laiks_txt, width=6).grid(row=0, column=ci, padx=2)
        ttk.Label(sest_frame, text="Sest", width=10).grid(row=1, column=0, sticky="w")
        for ci, _ in enumerate(sest_laiki):
            laika_indekss = 15 + ci
            pieejams = a.laiksPieejams(laika_indekss)
            krasa = "lightgreen" if pieejams else "lightgray"
            tk.Label(
                sest_frame,
                bg=krasa,
                width=3,
                height=1,
                relief='solid',
                bd=1
            ).grid(row=1, column=ci+1, padx=2, pady=1)

    def radit_grupu(notikums=None):
        '''
        Funkcija, kas apstrādā grupas/audzēkņa izvēli no saraksta.
        Atkarībā no režīma parāda grupas vai audzēkņa detaļas.
        '''
        nonlocal pasreizeja_grupa, pasreizejais_audzeknis, audzeknu_rindu_karte
        atlase = saraksta_logs.curselection()
        if not atlase:
            return
        
        veids = satura_veids.get()
        
        if veids == "audzekni":
            # ********* Audzēkņu režīms **********
            pasreizejais_audzeknis = saraksts[atlase[0]]
            pasreizeja_grupa = None
            radit_audzekna_detalas()
            
            # Notīrīt grupas detaļas
            detalu_virsraksts.config(text="Audzēknis izvēlēts")
            teksts_kods.config(text="Kods: —")
            teksts_laiks.config(text="Laiks: —")
            teksts_filiale.config(text="Filiāle: —")
            teksts_kurss.config(text="Kurss: —")
            teksts_skaits.config(text="Audzekņu skaits: —")
            teksts_vertejums.config(text="Vērtējums: —")
            audzeknu_saraksts.delete(0, 'end')
            return
        
        # ********* Grupu režīms **********
        pasreizeja_grupa = saraksts[atlase[0]]
        pasreizejais_audzeknis = None
        
        # Atjaunot virsrakstu
        if pasreizeja_grupa.Komplekteta:
            detalu_virsraksts.config(text=f"Komplektēta grupa: {pasreizeja_grupa.Kods}")
        else:
            detalu_virsraksts.config(text=f"Grupa: {pasreizeja_grupa.Kods}")
        
        # Atjaunot grupas informāciju
        teksts_kods.config(text=f"Kods: {pasreizeja_grupa.Kods}")
        teksts_laiks.config(text=f"Laiks: {stringLaiks(pasreizeja_grupa.Laiks)}")
        teksts_filiale.config(text=f"Filiāle: {pasreizeja_grupa.Filiale}")
        teksts_kurss.config(text=f"Kurss: {pasreizeja_grupa.Kurss}")
        teksts_skaits.config(text=f"Audzekņu skaits: {len(pasreizeja_grupa.Audzekni)}")
        teksts_vertejums.config(text=f"Vērtējums: {pasreizeja_grupa.Vertejums}")
        
        # Atjaunot audzēkņu sarakstu
        audzeknu_saraksts.delete(0, 'end')
        audzeknu_rindu_karte.clear()
        
        if pasreizeja_grupa.Audzekni:
            for i, a in enumerate(pasreizeja_grupa.Audzekni, 1):
                audzeknu_saraksts.insert('end', f"{i}. {a.Vards}")
        else:
            audzeknu_saraksts.insert('end', "Nav audzekņu")
        
        notirit_audzekna_detalas()

    def audzekna_klikskis(notikums=None):
        nonlocal pasreizejais_audzeknis
        atlase = audzeknu_saraksts.curselection()
        if atlase and pasreizeja_grupa and pasreizeja_grupa.Audzekni:
            pasreizejais_audzeknis = pasreizeja_grupa.Audzekni[atlase[0]]
            radit_audzekna_detalas()

    audzeknu_saraksts.bind('<<ListboxSelect>>', audzekna_klikskis)
    dzest_audzekni_poga.config(command=dzest_atlasito_audzekni)
    dzest_audzekni_poga.state(['disabled'])

    def radit_audzekna_detalas():
        '''Atjauno audzēkņa detaļu laukus ar pašreizējā audzēkņa informāciju'''
        if not pasreizejais_audzeknis:
            notirit_audzekna_detalas()
            return
        
        a = pasreizejais_audzeknis
        aud_teksts_vards.config(text=f"Vārds: {a.Vards}")
        aud_teksts_perspk.config(text=f"Personas kods: {a.PersKods}")
        aud_teksts_talr.config(text=f"Tālrunis: {a.TelNr}")
        aud_teksts_epasts.config(text=f"E-pasts: {a.Epasts}")
        aud_teksts_filiales.config(text=f"Filiāles: {', '.join(a.Filiales)}")
        aud_teksts_kursi.config(text=f"Kursi: {', '.join(a.Kursi)}")
        
        if hasattr(a, 'Pieejamiba'):
            aud_teksts_pieejamiba.config(text=f"Pieejamība: {a.Pieejamiba}")
        else:
            aud_teksts_pieejamiba.config(text="Pieejamība: —")

        uzzimet_pieejamibu(a)
        dzest_audzekni_poga.state(['!disabled'])

    # ******** Notikumu sasaistes *********
    saraksta_logs.bind('<<ListboxSelect>>', radit_grupu)  # Izvēles maiņa
    saraksta_logs.bind('<Double-1>', radit_grupu)  # Dubultklikšķis
    
    # grupu saraksta atjaunošanai pie filtru maiņas
    izveleta_filiale.trace_add('write', lambda *_: ieladet_grupas())
    izveletais_kurss.trace_add('write', lambda *_: ieladet_grupas())

    def pie_aizversanas():
        '''Automātiski saglabā plānojumu, kad aizver logu'''
        DM.saglabatPlanojumu(planojums)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", pie_aizversanas)

    # Sākotnējā ielāde
    ieladet_grupas()
    root.mainloop()

def PlanojumuSkats():
    '''
    Plānojumu izvēles logs. Attēlo pieejamos plānojumus un ļauj tos atvērt, izveidot vai dzēst.
    Satur meklēšanas funkcionalitāti plānojumu filtrēšanai.
    '''
    root = tk.Tk()
    root.title("Plānojumi")
    root.geometry("800x600")
    lapa = ttk.Frame(root, padding=12)
    lapa.pack(fill='both', expand=True)
    ttk.Label(lapa, text="Izvēlies plānojumu", font=font.Font(size=18, weight="bold")).pack(anchor="center")

    # ********* Meklēšanas sadaļa *********
    mekletais = tk.StringVar()
    meklesanas_sadala = ttk.Frame(lapa)
    meklesanas_sadala.pack(fill='x', pady=(8, 6))
    ttk.Label(meklesanas_sadala, text="Meklēt:").pack(side='left', padx=(0,6))
    meklesanas_lauks = ttk.Entry(meklesanas_sadala, textvariable=mekletais)
    meklesanas_lauks.pack(side='left', fill='x', expand=True)

    # ********* Plānojumu saraksta sadaļa *********
    planojumu_sadala = ttk.Frame(lapa)
    planojumu_sadala.pack(fill='both', expand=True)
    planojumu_saraksts = tk.Listbox(planojumu_sadala, activestyle='none', height=15, selectmode="single")
    planojumu_saraksts.pack(side='left', fill='both', expand=True)
    ritjosla = ttk.Scrollbar(planojumu_saraksts, orient='vertical', command=planojumu_saraksts.yview)
    ritjosla.pack(side='right', fill='y')
    planojumu_saraksts.config(yscrollcommand=ritjosla.set)

    # ****** Pogas **********
    pogu_sadala = ttk.Frame(lapa)
    pogu_sadala.pack(fill='x', pady=(8,0))
    atvert = ttk.Button(pogu_sadala, text="Atvērt", width=12)
    jauns = ttk.Button(pogu_sadala, text="Jauns", width=12)
    atsvaidzinat = ttk.Button(pogu_sadala, text="Atsvaidzināt", width=12)
    dzest = ttk.Button(pogu_sadala, text="Dzēst", width=12)
    aizvert = ttk.Button(pogu_sadala, text="Aizvērt", width=12, command=root.destroy)
    atvert.pack(side='left', padx=(0,6))
    jauns.pack(side='left', padx=(0,6))
    atsvaidzinat.pack(side='left', padx=(0,6))
    dzest.pack(side='left', padx=(0,6))
    aizvert.pack(side='right')

    planojumi = []
    
    def iegut_sarakstu():
        '''Ielādē un filtrē plānojumu sarakstu pēc meklēšanas vārda'''
        nonlocal planojumi
        planojumi = DM.visiPlanojumi()
        filtretais = mekletais.get().lower()
        planojumu_saraksts.delete(0, 'end')
        for datne, datums in planojumi:
            # Noņemt datnes paplašinājumu
            nosaukums = "".join(datne.split('.')[:-1:])
            # Pārbaudīt, vai atbilst meklēšanas filtram
            if filtretais == "" or filtretais in nosaukums.lower():
                # Attēlot nosaukumu ar datumu un laiku
                planojumu_saraksts.insert('end', f"{nosaukums}  ({datums})")
    
    def atvert_izveleto(notikums=None):
        '''Atver izvēlēto plānojumu'''
        atlase = planojumu_saraksts.curselection()
        if not atlase:
            messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies plānojumu.")
            return
        plans_ar_datumu = planojumu_saraksts.get(atlase[0])
        # Atdalīt nosaukumu no datuma (pirms pēdējās iekavas)
        plans = plans_ar_datumu.split('  (')[0]
        atvertPlanojumu(plans, root)
    
    def jauns_planojums():
        '''
        Izveido jaunu plānojumu.
        Ļauj izvēlēties CSV failu ar klientu datiem un ievadīt plānojuma nosaukumu.
        '''
        # Datnes izvēles logs
        csv_fails = filedialog.askopenfilename(
            title="Izvēlies CSV failu ar klientu datiem",
            filetypes=[("CSV faili", "*.csv"), ("Visi faili", "*.*")]
        )
        
        if not csv_fails:
            return
        
        # Nosaukuma ievades dialogs
        nosaukuma_logs = tk.Toplevel()
        nosaukuma_logs.title("Jauns plānojums")
        nosaukuma_logs.geometry("400x150")
        nosaukuma_logs.transient()
        nosaukuma_logs.grab_set()
        
        galvena_sadala = ttk.Frame(nosaukuma_logs, padding=12)
        galvena_sadala.pack(fill='both', expand=True)
        
        ttk.Label(galvena_sadala, text="Plānojuma nosaukums:", font=font.Font(weight="bold")).pack(anchor="w", pady=(0,8))
        ttk.Label(galvena_sadala, text="(tikai burti, cipari, '-' un '_')", font=font.Font(size=9), foreground='gray').pack(anchor="w", pady=(0,4))
        
        nosaukuma_main = tk.StringVar()
        nosaukuma_ievade = ttk.Entry(galvena_sadala, textvariable=nosaukuma_main, width=40)
        nosaukuma_ievade.pack(fill='x', pady=(0,12))
        nosaukuma_ievade.focus()
        
        pogu_sadala = ttk.Frame(galvena_sadala)
        pogu_sadala.pack(fill='x')
        
        def izveidot():
            '''Pārbauda nosaukumu un izveido jaunu plānojumu'''
            nosaukums = nosaukuma_main.get().strip()
            if not nosaukums:
                messagebox.showwarning("Brīdinājums", "Lūdzu, ievadi plānojuma nosaukumu.")
                return
            
            # Validācija - tikai burti, cipari, '-' un '_'
            if not re.match(r'^[a-zA-Z0-9_-]+$', nosaukums):
                messagebox.showerror("Kļūda", "Plānojuma nosaukumā drīkst izmantot tikai:\n• Burtus (a-z, A-Z)\n• Ciparus (0-9)\n• Domuzīmes (-)\n• Apakšsvītras (_)")
                return
            
            try:
                # Izveidot jaunu plānojumu
                jauns_planojums = Planojums(nosaukums)
                
                # Ielasīt klientu datus no CSV
                DM.ielasitKlientuDatus(csv_fails, jauns_planojums)
                
                # Ģenerēt grupas
                jauns_planojums.generetGrupas()
                
                # Saglabāt
                DM.saglabatPlanojumu(jauns_planojums)
                
                messagebox.showinfo("Izdevās", f"Plānojums '{nosaukums}' veiksmīgi izveidots.")
                nosaukuma_logs.destroy()
                iegut_sarakstu()
                
            except Exception as e:
                messagebox.showerror("Kļūda", f"Nevarēja izveidot plānojumu: {str(e)}")
        
        def atcelt():
            '''Aizver logu bez plānojuma izveides'''
            nosaukuma_logs.destroy()
        
        ttk.Button(pogu_sadala, text="Izveidot", command=izveidot).pack(side='left', padx=(0,6))
        ttk.Button(pogu_sadala, text="Atcelt", command=atcelt).pack(side='left')
    
    def dzest_izveleto():
        '''Dzēš izvēlēto plānojumu pēc apstiprinājuma'''
        atlase = planojumu_saraksts.curselection()
        if not atlase:
            messagebox.showwarning("Brīdinājums", "Lūdzu, izvēlies plānojumu.")
            return
        plans_ar_datumu = planojumu_saraksts.get(atlase[0])
        # Atdalīt nosaukumu no datuma
        plans = plans_ar_datumu.split('  (')[0]
        
        if messagebox.askyesno("Apstiprināšana", f"Vai tiešam gribā dzēst plānojumu '{plans}'?"):
            try:
                # Izsaukt database_manager funkciju plānojuma dzēšanai
                DM.dzestPlanojumu(plans)
                messagebox.showinfo("Izdevās", f"Plānojums '{plans}' veiksmīgi dzēsts.")
                iegut_sarakstu()
            except Exception as e:
                messagebox.showerror("Kļūda", f"Nevarēja dzēst plānojumu: {str(e)}")
    
    def mainas_teksts(*_):
        '''Callback funkcija, kas tiek izsaukta, kad mainās meklēšanas teksts'''
        iegut_sarakstu()
    
    # ******** Notikumu sasaistes *********
    planojumu_saraksts.bind('<Double-1>', atvert_izveleto)
    atvert.config(command=atvert_izveleto)
    jauns.config(command=jauns_planojums)
    atsvaidzinat.config(command=iegut_sarakstu)
    dzest.config(command=dzest_izveleto)
    mekletais.trace_add('write', mainas_teksts)
    
    # Sākotnējā saraksta ielāde
    iegut_sarakstu()
    root.mainloop()