import tkinter as tk

class Zakljucek():

    def __init__(self, master):
        self.master = master
        master.geometry('200x100')

        zmagovalec = tk.Label(master, text='Tukaj napišemo zmagovalca')
        zmagovalec.grid(row=0, column=0, columnspan = 5)

        vprasanje = tk.Label(master, text='Kaj želiš narediti sedaj?')
        vprasanje.grid(row=1, column=0, columnspan = 5)

        gumb_na_novo = tk.Button(master, text='Nova igra',
                          command=self.zacni_novo)
        gumb_na_novo.grid(row=2, column=1)
        
        gumb_ista = tk.Button(master, text='Ponovno igraj',
                          command=self.ponovi_igro)
        gumb_ista.grid(row=2, column=3)

    def zacni_novo(self):
        print('gremo v začetni meni')
        self.zacetni_master.deiconify()
        self.master.destroy()
        self.gui_master.destroy()

    def ponovi_igro(self):
        print('Ponovno izrišemo isto platno')
        self.gui_master.destroy()
        self.zacetni.zacni_igro()
        self.master.destroy()
