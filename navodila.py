import tkinter as tk
import os

class Navodila:

    def __init__(self, master):
        self.master = master

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')

        #Vse slike:
        #self.slika_ozadje_id = tk.PhotoImage(file=os.path.join('slike', 'pergament.gif'))
        self.slika_prvic_id = tk.PhotoImage(file=os.path.join('slike', 'prvic_v_polju.gif'))
        self.slika_ponovno_id = tk.PhotoImage(file=os.path.join('slike', 'ponovno_v_polju.gif'))
        self.slika_rob_id = tk.PhotoImage(file=os.path.join('slike', 'na_robu.gif'))

        #Vsi napisi
        naslov = "Navodila igre"
        napis1 = "Cilj igre je pripeljati žogo v svoj gol. Vsakemu igralcu smer \
igre kaže puščica v njegovi barvi, kadar je na vrsti. \
Igralca izmenično premikata isto žogo, pri tem veljajo pravila:\n\n\
      - Žoge ne moremo brcniti dvakrat po isti poti.\n\
      - Vsak igralec se lahko premakne v vseh 8 različnih smereh (tudi po diagonali), če pot še ni bila igrana.\n\
      - Če igralec brcne žogo v točko, kjer je žoga že kdaj prej bila, jo lahko brcne še enkrat. "

        napis2 = "Posebna pravila na robu:\n\
      - Žoga se od roba odbije, isti igralec je na vrsti še enkrat.\n\
      - Pot po robu ni mogoča."

        napis3 = "Lahko se zgodi, da nimamo več nobene možne poti iz polja \
kjer se nahajamo. V tem primeru je igra izenačena. Igra se \
konča, če pride do izenačenja, ali eden izmed igralcev zadane gol."

        #slika_ozadje = self.polje.create_image(0, 0, anchor="nw", image=self.slika_ozadje_id)
        self.polje.create_text(20, 15, anchor="nw", text=naslov)
        self.polje.create_text(20, 30, anchor="nw", text=napis1, width=350)
        self.polje.create_image(20, 190, anchor="nw", image=self.slika_prvic_id)
        self.polje.create_image(200, 190, anchor="nw", image=self.slika_ponovno_id)
        self.polje.create_text(20, 380, anchor="nw", text=napis2, width=350)
        self.polje.create_image(80, 430, anchor="nw", image=self.slika_rob_id)
        self.polje.create_text(20, 600, anchor="nw", text=napis3, width=350)
        
        gumb_igraj = tk.Button(master, text='Nazaj', command=self.master.destroy)
        gumb_igraj.pack()

        self.master.attributes("-topmost", True)

        self.master.geometry("390x700")

        
