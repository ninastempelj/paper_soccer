import threading


class Racunalnik:

    def __init__(self, gui, algoritem):
        self.gui = gui
        self.stevec_korakov = 0  # števec doslej izrisanih korakov
        self.poteza = []  # tu se bo shranila poteza
        self.algoritem = algoritem
        self.mislec = None

    def povleci_potezo(self):
        """Požene algoritem na kopiji igre - požene vlakno."""
        # Ko se začne poteza, ponastavimo števec korakov:
        self.stevec_korakov = 0
        # Ustvarimo vlakno:
        self.mislec = \
            threading.Thread(target=lambda:
                    self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
        # Poženemo vlakno:
        self.mislec.start()
        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.polje.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, shrani si jo, da jo mora narediti
            self.poteza = self.algoritem.poteza
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
            # s tem klicem začnemo res izvajati potezo (po korakih)
            self.povleci_korak()
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.polje.after(100, self.preveri_potezo)

    def povleci_korak(self):
        """Ko enkrat računalnik naračuna celo potezo,
        jo tu narišemo po posameznih korakih."""
        # Prvi element poteze je trenutni položaj,
        # zato števec povečamo pred risanjem:
        self.stevec_korakov += 1
        self.gui.polje.after(300, lambda: self.gui.povleci_korak(
                                  self.poteza[self.stevec_korakov]))

    def klik(self, novo):
        """Računalnik ignorira klik."""
        pass

    def prekini(self):
        """Če kdo zapre okno ali drugače nasilno prekine razmišljanje.
        To metodo kliče GUI, če je treba prekiniti razmišljanje. """
        if self.mislec:
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None
