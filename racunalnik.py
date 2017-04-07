
class Racunalnik:

     def __init__(self, gui):
        self.gui = gui
        self.stevec = 0
        self.polja = []

     def povleci_potezo(self, staro):
          self.zadnji_polozaj = staro
          self.stevec = 0
          self.polja = [staro,(5,6),(7,3)]
          # kliče algoritem, nastavi self.poteze na nasledno

     def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira.
        pass

     def povleci_korak(self):
        self.stevec += 1
        self.gui.povleci_korak(self.polja[stevec-1], self.polja[stevec])
        pass

     def klik(self, staro, novo):
        # Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.
        pass

