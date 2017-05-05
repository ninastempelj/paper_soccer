import tkinter as tk


class Zakljucek:

    def __init__(self, master, napis, zacetni_meni, gui):
        self.master = master              # zaključno okno
        self.zacetni_meni = zacetni_meni  # objekt na začetnem oknu
        self.gui = gui   # objekt GUI
        master.geometry('200x100')

        rezultat = tk.Label(master, text=napis)
        rezultat.grid(row=0, column=0, columnspan=5)

        vprasanje = tk.Label(master, text='Kaj želiš narediti sedaj?')
        vprasanje.grid(row=1, column=0, columnspan=5)

        gumb_na_novo = tk.Button(master, text='Nova igra',
                                 command=self.zacni_novo_igro)
        gumb_na_novo.grid(row=2, column=1)

        gumb_ista = tk.Button(master, text='Ponovno igraj',
                              command=self.ponovi_igro)
        gumb_ista.grid(row=2, column=3)

        master.attributes("-topmost", True)

    def zacni_novo_igro(self):
        """Ponovno odpre začetni meni."""
        self.zacetni_meni.master.deiconify()
        self.gui.master.destroy()
        self.master.destroy()

    def ponovi_igro(self):
        """Narišemo čisto polje, igramo še enkrat z istimi nastavitvami."""
        self.gui.master.destroy()
        self.zacetni_meni.zacni_igro()
        self.master.destroy()
