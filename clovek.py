
class Clovek:
    
    def __init__(self, gui):
        self.gui = gui

    def povleci_potezo(self):
        # to funkcijo rabi samo računalnik - kot pri Bauerju igraj
        pass

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        # Človek jo lahko ignorira
        pass

    def klik(self, novo):
        """Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič."""
        self.gui.povleci_korak(novo)

    def povleci_korak(self):
        # za računalnik je drugače, če vleče korak ali potezo, zato še ta.
        # Človek v obeh primerih čaka na klik uporabnika.
        pass
