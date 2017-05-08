import tkinter as tk
import os


class Navodila:

    def __init__(self, master):
        self.master = master

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')

        # Vse slike:
        master.slika_ozadje_id = tk.PhotoImage(
            file=os.path.join('slike', 'pergament.gif'))
        master.slika_prvic_id = tk.PhotoImage(
            file=os.path.join('slike', 'prvic_v_polju.GIF'))
        master.slika_ponovno_id = tk.PhotoImage(
            file=os.path.join('slike', 'ponovno_v_polju.gif'))
        master.slika_rob_id = tk.PhotoImage(
            file=os.path.join('slike', 'na_robu.gif'))

        # Vsi napisi
        naslov = "Navodila igre"
        napis1 = "Cilj igre je pripeljati žogo v svoj gol. " \
                 "Vsakemu igralcu smer igre kaže puščica v njegovi barvi," \
                 " kadar je na vrsti. Igralca izmenično premikata isto žogo," \
                 " pri tem veljajo pravila:\n\n" \
                 "  - Žoge ne moremo brcniti dvakrat po isti poti.\n" \
                 "  - Vsak igralec se lahko premakne v vseh 8 različnih smereh" \
                 " (tudi po diagonali), če pot še ni bila igrana.\n" \
                 "  - Če igralec brcne žogo v točko, kjer je žoga že kdaj " \
                 "prej bila, jo lahko brcne še enkrat. "

        napis2 = "Posebna pravila na robu:\n\n" \
                 "  - Žoga se od roba odbije, isti igralec je na vrsti " \
                 "še enkrat.\n" \
                 "  - Pot po robu ni mogoča."

        napis3 = "Lahko se zgodi, da nimamo več nobene možne poti iz polja, " \
                 "kjer se nahajamo. V tem primeru je igra izenačena. " \
                 "Igra se konča, če pride do izenačenja, ali eden izmed " \
                 "igralcev zadane gol."

        self.polje.create_image(0, 5, anchor="nw", image=master.slika_ozadje_id)
        self.polje.create_text(160, 25, anchor="nw", text=naslov, font="Helvetica 12 bold")
        self.polje.create_text(55, 50, anchor="nw", text=napis1, width=345)
        self.polje.create_image(60,190, anchor="nw", image=master.slika_prvic_id)
        self.polje.create_image(230, 190, anchor="nw",image=master.slika_ponovno_id)
        self.polje.create_text(55, 313, anchor="nw", text=napis2, width=345)
        self.polje.create_image(160, 380, anchor="nw", image=master.slika_rob_id)
        self.polje.create_text(55, 486, anchor="nw", text=napis3, width=345)
        gumb_nazaj = tk.Button(master, text='Nazaj',
                               command=self.master.destroy)
        self.polje.create_window(230,580, window=gumb_nazaj)

        self.master.attributes("-topmost", True)

        self.master.geometry("450x650")
