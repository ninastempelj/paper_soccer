import tkinter as tk


class Navodila:

    def __init__(self, master):
        self.master = master

        polje = tk.Canvas(master)

        napis1 = "adgkljč ćfidjać gkjaćdkgajć kdfaćkldf ać '\n' \
                  dčklćsakjgda kjačfk čkfadfkl ać"

        #slika1 =

        napis2 = "časdćjkć"

        tekst = polje.create_text(100, 100, text=napis1)
        
