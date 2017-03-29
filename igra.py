class Igra():
    def __init__(self):
        self.sirina=9 #TODO kako dobiš te podatke iz gui-ja
        self.visina=13
        self.plosca=[[set() for j in range(self.sirina)]
                     for i in range(self.visina)]
        self.smeri=list(range(-4,4))

        seznam_neproblematicnih=list(range(int((self.sirina-1)/2-1)))+list(
            range(int((self.sirina-1)/2+1),self.sirina))
        for i in seznam_neproblematicnih:
            self.plosca[0][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[-1][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[1][i] |= {-3,-4,1,-2,2}
            self.plosca[-1][i] |= {-1,4,3,2,-2}
        for i in range(1,self.visina):
            self.plosca[i][0] |= {-3,-2,-1,4,-4}
            self.plosca[i][-1] |= {1,2,3,-4,4}
        #Gol zgoraj
        self.plosca[0][int((self.sirina-1)/2)] |={4,-1,-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2+1)] |={-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2)+2] |={-2,-3,-4,1,2,3,4}
        self.plosca[1][int((self.sirina-1)/2)] |={-2,-3,-4}
        self.plosca[1][int((self.sirina-1)/2+2)] |={-4,1,2}
        
        #Gol spodaj
        self.plosca[-1][int((self.sirina-1)/2)] |={2,3,4,-1,-2,-3,-4}
        self.plosca[-1][int((self.sirina-1)/2+1)] |={-2,2,3,4,-1}
        self.plosca[-1][int((self.sirina-1)/2)+2] |={-4,1,2,3,4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2)] |={4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2+2)] |={2,3,4}
        print(self.plosca)
        

            
        
        
        
