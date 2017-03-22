import tkinter as tk

class GUI():
    def __init__(self.master):
        (self.sirna, self.visina) = (9, 13) #Štejemo število oglišč
        self.sirina_kvadratka = 100
        self.od_roba = 100

        self.polje = tk.Canvas(master)
        self.polje.pack()

        self.polje.create_line(self.od_roba + (self.sirina-3)/2)
        self.oglisca = [[(self.od_roba + j*self.sirina_kvadratka, self.od_roba + i* self.sirina_kvadratka) for j in range(self.sirina)] for i in range(self.visina)]
            :
                vrstica.
                    ]
        
