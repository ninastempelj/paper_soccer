class Clovek:
    
    def __init__(self, gui):
        self.gui = gui

    def povleci_potezo(self):
        """To funkcijo potrebuje samo računalnik."""
        pass

    def prekini(self):
        """Če kdo zapre okno ali drugače nasilno prekine razmišljanje.
        To metodo kliče GUI, če je treba prekiniti razmišljanje. """
        pass

    def klik(self, novo):
        """Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič."""
        self.gui.povleci_korak(novo)

    def povleci_korak(self):
        """To funkcijo potrebuje samo računalnik."""
        pass
