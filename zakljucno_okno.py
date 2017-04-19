import tkinter as tk

class Zakljucek():

    def __init__(self, master, napis, zacetni_meni, zacetno_okno, gui):
        self.master = master
        self.zacetni_meni = zacetni_meni
        self.zacetno_okno = zacetno_okno
        self.gui = gui
        master.geometry('200x100')

        zmagovalec = tk.Label(master, text = napis)
        zmagovalec.grid(row=0, column=0, columnspan = 5)

        vprasanje = tk.Label(master, text='Kaj želiš narediti sedaj?')
        vprasanje.grid(row=1, column=0, columnspan = 5)

        gumb_na_novo = tk.Button(master, text='Nova igra',
                          command=self.zacni_novo)
        gumb_na_novo.grid(row=2, column=1)

        gumb_ista = tk.Button(master, text='Ponovno igraj',
                          command=self.ponovi_igro)
        gumb_ista.grid(row=2, column=3)

        master.attributes("-topmost", True)

    def zacni_novo(self):
        #print('gremo v začetni meni')
        self.zacetno_okno.deiconify()
        self.gui.master.destroy()
        self.master.destroy()

    def ponovi_igro(self):
        #print('Ponovno izrišemo isto platno')
        self.gui.master.destroy()
        self.zacetni_meni.zacni_igro()
        self.master.destroy()

## TODO če X zapri VSE!!!!!!!!!!
