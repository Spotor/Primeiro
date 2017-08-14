from tkinter import *
 
class no:
    def __init__(self, info=None):
        self.esquerdo = None
        self.direito = None
        self.info = info
 
    def __str__(self):
        return "{", str(info), "}"
     
    def ramo(self):
        folha_esq = 0
        if self.esquerdo:
            folha_esq = self.esquerdo.ramo()
        folha_dir = 0
        if self.direito:
            folha_dir = self.direito.ramo()
        return 1 + max(folha_esq, folha_dir)
 
    def defilhos(self, esquerdo, direito):
        self.esquerdo = esquerdo
        self.direito = direito
 
    def balanceamento(self):
        folha_esq = 0
        if self.esquerdo:
            folha_esq = self.esquerdo.ramo()
        folha_dir = 0
        if self.direito:
            folha_dir = self.direito.ramo()
        return folha_esq - folha_dir
 
class ArvoreAVL:
 
    def __init__(self):
        self.raiz = None
 
    def criaNoh(self, info):
        return no(info)
 
    def calcmax(self, raiz):
        if raiz == None:
            return 0
        return raiz.ramo()
 
    def contaNohs(self, raiz):
        if raiz == None:
            return 0
        return 1 + self.contaNohs(raiz.esquerdo) + self.contaNohs(raiz.direito)
 
    def RE(self, raiz):
        if raiz:
            raiz.info, raiz.direito.info = raiz.direito.info, raiz.info
            old_esquerdo = raiz.esquerdo
            raiz.defilhos(raiz.direito, raiz.direito.direito)
            raiz.esquerdo.defilhos(old_esquerdo, raiz.esquerdo.esquerdo)
 
    def RD(self, raiz):
        if raiz:
            raiz.info, raiz.esquerdo.info = raiz.esquerdo.info, raiz.info
            old_direito = raiz.direito
            raiz.defilhos(raiz.esquerdo.esquerdo, raiz.esquerdo)
            raiz.direito.defilhos(raiz.direito.direito, old_direito)
 
    def RED(self, raiz):
        if raiz:
            self.RE(raiz.esquerdo)
            self.RD(raiz)
 
    def RDE(self, raiz):
        if raiz:
            self.RD(raiz.direito)
            self.RE(raiz)
 
    def balancear(self, raiz):
        if raiz:
            balanco = raiz.balanceamento()
 
            if balanco > 1:
                if raiz.esquerdo.balanceamento() > 0:
                    self.RD(raiz)
                else:
                    self.RED(raiz)
            elif balanco < -1:
                if raiz.direito.balanceamento() < 0:
                    self.RE(raiz)
                else:
                    self.RDE(raiz)
 
    def insere(self, raiz, info):
        if raiz == None:
            return self.criaNoh(info)
        else:
            if info <= raiz.info:
                raiz.esquerdo = self.insere(raiz.esquerdo, info)
            else:
                raiz.direito = self.insere(raiz.direito, info)
 
            self.balancear(raiz)
 
        return raiz
 
 
class Aplicacao:
    def __init__(self, pai):
        self.arvoreAVL = None
        self.t1 = Entry(pai)
        self.t1.bind("<Return>", self.constroiArvore)
        self.t1.pack()
 
        self.b1 = Button(pai,height = 1, width = 20)
        self.b1.bind("<Button-1>", self.constroiArvore)
        self.b1["text"] = "Insere um Valor"
 
        self.b1.pack()
 
        self.b2 = Button(pai,height = 1, width = 20)
        self.b2["text"] = "Exibe Árvore"
        self.b2.bind("<Button-1>", self.exibeArvoreAVL)
        self.b2.pack()
 
        self.b3 = Button(pai,height = 1, width = 20)
        self.b3["text"] = "Fatores de Balanceamento"
        self.b3.bind("<Button-1>", self.plotabalanco)
        self.b3.pack()
 
        self.c1 = Canvas(pai, width=1024, height=650)
        self.c1.pack()
 
    def constroiArvore(self, *args):
        try:
            valor = int(self.t1.get())
        except Exception:
            return
        print(valor)
        if self.arvoreAVL == None:
            print("Criando")
            self.arvoreAVL = ArvoreAVL()
            self.raiz = self.arvoreAVL.criaNoh(valor)
        else:
            print("Inserindo")
            self.arvoreAVL.insere(self.raiz, valor)
        self.desenhaArvore(False)
 
    def exibeArvoreAVL(self, *args):
        if self.arvoreAVL != None:
            print("Exibindo arvore")
            self.desenhaArvore(False)
 
    def plotabalanco(self, *args):
        if self.arvoreAVL != None:
            print("Exibindo arvore")
            self.desenhaArvore(True)
 
    def desenhaArvore(self, comFB=False):
        self.HORIZONTAL = 1024
        self.VERTICAL = 750
        self.tamanho = 30
        self.c1.delete(ALL)
        self.c1.create_rectangle(
            0, 0, self.HORIZONTAL, self.VERTICAL, fill="Black")
        self.xmax = self.c1.winfo_width() - 40
        self.ymax = self.c1.winfo_height()
        self.numero_linhas = self.arvoreAVL.calcmax(self.raiz)
        x1 = int(self.xmax / 2 + 20)
        y1 = int(self.ymax / (self.numero_linhas + 1))
        self.desenhaNoh(self.raiz, x1, y1, x1, y1, 1, comFB)
 
    def desenhaNoh(self, noh, posAX, posAY, posX, posY, linha, comFB=False):
        if noh == None:
            return
        numero_colunas = 2 ** (linha + 1)
        x1 = int(posX - self.tamanho / 2)
        y1 = int(posY - self.tamanho / 2)
        x2 = int(posX + self.tamanho / 2)
        y2 = int(posY + self.tamanho / 2)
        self.c1.create_line(posAX, posAY, posX, posY, fill="blue")
        self.c1.create_oval(x1, y1, x2, y2, fill="yellow")
 
        rotulo = str(noh.info)
 
        if comFB:
            rotulo = str(noh.balanceamento())
 
        self.c1.create_text(posX, posY, text=str(rotulo))
        posAX, posAY = posX, posY
        dx = self.xmax / numero_colunas
        dy = self.ymax / (self.numero_linhas + 1)
        posX = posAX + dx
        posY = posAY + dy
        self.desenhaNoh(noh.direito, posAX, posAY, posX, posY, linha + 1, comFB)
        posX = posAX - dx
        self.desenhaNoh(noh.esquerdo, posAX, posAY, posX, posY, linha + 1, comFB)
 
root = Tk(None, None, "Arvore -AVL- Balanceamento")
root.geometry("800x600")
ap = Aplicacao(root)
root.mainloop()
