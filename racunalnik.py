import threading
import time
import minimax

class Racunalnik:

     def __init__(self, gui, algoritem):
        self.gui = gui
        self.stevec_korakov = 0
        self.naslednja_polja = []
        self.algoritem = algoritem
        self.mislec = None

     def povleci_potezo(self):
          #self.zadnji_polozaj = self.gui.igra.zadnji_polozaj
          self.stevec_korakov = 0
          #verjetno neuporabno self.naslednja_ polja = [staro,(5,6),(7,3)] začasno

          # kliče algoritem, nastavi self.poteze na nasledno
          self.mislec = threading.Thread(
               target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
          # Poženemo vlakno:
          self.mislec.start()

          # Gremo preverjat, ali je bila najdena poteza:
          self.gui.polje.after(100, self.preveri_potezo)

     def preveri_potezo(self):
          """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
          #staro = self.gui.igra.zadnji_polozaj ## A TO RABMO?
          #print("Računalnik preverja ali je že poteza")
          if self.algoritem.poteza is not None:
               print("pršu 1")
               # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
               self.naslednja_polja = self.algoritem.poteza
               # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
               print("Računalnik našel potezo: ", self.naslednja_polja)
               self.mislec = None
               self.povleci_korak()
          else:
               #print("pršu2")
               # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
               self.gui.polje.after(100, self.preveri_potezo)

     def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
         if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

     def povleci_korak(self):
        self.stevec += 1
        print("čakam")
        self.gui.polje.after(300,
                             lambda: self.gui.povleci_korak(self.naslednja_polja[self.stevec]))

     def klik(self, novo):
        # Računalnik ignorira klik
        pass
