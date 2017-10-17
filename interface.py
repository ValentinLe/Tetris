
from tkinter import *
import time
from main import *
from tkinter.filedialog import *

class Interface:
    def __init__(self,fen,sizeX,sizeY,b):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.b = b
        self.grille = self.b.tempL
        self.rectangle_last_piece = []
        self.can_move = True

        self.color = color = {'purple':'#b800e6','cyan':'#00b8e6',
                              'yellow':'#e6e600','orange':'#ff751a','blue':'#0047b3',
                              'red':'#ff1c1c','green':'#35e701'}
        
        self.fen = fen
        self.fen.wm_title("Tetris")

        cdg = Frame(self.fen)
        cdd = Frame(self.fen)
        cdg.pack(side=LEFT)
        cdd.pack(side=RIGHT)
        
        self.cv = Canvas(self.fen,width=self.sizeX*30+2,height=self.sizeY*30+2,bg="#595959")
        self.cv.pack()
        self.cv.create_line(0,2*30+2,self.sizeX*30+4,2*30+2,width=2,fill="white")

        lab_record = Label(cdd,text="Record")
        lab_record.pack()
        self.text_record = Text(cdd,width=10,height=1)
        self.text_record.pack()
        self.text_record.config(state=DISABLED)

        self.cv_next = Canvas(cdd,width=4*30+2+30,height=4*30+2+30,bg="#595959")
        self.cv_next.pack(padx=5)

        bj = Button(cdd,text="Jouer",font="monospace 10",command=self.bjouer)
        bj.pack(pady=20)

        lab_score = Label(cdd,text="Score")
        lab_score.pack()
        self.text_score = Text(cdd,width=10,height=1)
        self.text_score.pack()
        lab_level = Label(cdd,text="Level")
        lab_level.pack()
        self.text_level = Text(cdd,width=5,height=1)
        self.text_level.pack()
        self.text_score.config(state=DISABLED)
        self.text_level.config(state=DISABLED)

        bquit = Button(cdd,text="Quitter",font="monospace 10",command=self.quit)
        bquit.pack(pady=20)

        self.fen.bind('<KeyPress>', self.moves)
        self.fen.focus_set()

    def rien(self):
        return

    def bjouer(self):
        pieces = [T,Barre,Carre,L,L_,Z,Z_]
        self.b.party_proced = False
        b = Board(10,24,Piece(Carre),Piece(choice(pieces)),0)
        self.b = b
        self.dessiner_grille(b.L)
        mon_thread=Thread(target=main,args=(self.fen,b,self))
        mon_thread.start()

    def test(self):
        return self.dessinerGrille(self.grille)

    def moves(self,event):
        if self.can_move:
            self.can_move = False
            touche = event.keysym
            if touche=='Right' and self.b.move_possible(1):
                self.b.piece.j += 1
                self.dessiner_piece()
            elif touche=='Left' and self.b.move_possible(-1):
                self.b.piece.j -= 1
                self.dessiner_piece()
            elif touche=='Up' and not(isinstance(self.b.piece.name_piece,Carre)):
                self.b.piece.name_piece.form = self.b.turn_piece()
                self.dessiner_piece()
            elif touche=='Down':
                self.b.time_sleep=0.02
            elif touche=='space':
                self.b.time_sleep=0
        self.can_move = True
    
    def dessiner_grille(self,g):
        self.cv.delete(ALL)
        self.cv.create_line(0,2*30+2,self.sizeX*30+4,2*30+2,width=2,fill="white")
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                self.dessiner_case(30,i,j,self.grille[i][j]) 

    def dessiner_case(self,cote,i,j,case):
        x0,y0 = (cote)*j+2,(cote)*i+2
        x1,y1 = x0 + cote, y0 + cote
        xm,ym = x0 + cote//2,y0 + cote//2

        if case != None:
            self.cv.create_rectangle(x0,y0,x1,y1,fill=self.color[case.color],outline="white")

    def dessiner_piece(self):
        for x in self.rectangle_last_piece:
            self.cv.delete(x)
        self.rectangle_last_piece = []
        for x in self.b.piece.name_piece.form:
            i,j = self.b.piece.i,self.b.piece.j
            x0,y0 = 30*(x[1]+j)+2,30*(x[0]+i)+2
            x1,y1 = x0+30,y0+30
            self.rectangle_last_piece.append(self.cv.create_rectangle(x0,y0,x1,y1,fill=self.color[self.b.piece.name_piece.color],outline="white"))
        
            
    
    def dessiner_next_piece(self):
        self.cv_next.delete(ALL)
        cote = 32
        x0,y0 = 15+cote,2*cote+15
        x1,y1 = x0 + 30, y0 + 30
        
        l = self.b.next_piece.name_piece.form
    
        for x in l:
            x0_temp=x0+x[1]*cote
            y0_temp=y0+x[0]*cote
            x1_temp=x0_temp + cote
            y1_temp=y0_temp + cote
            self.cv_next.create_rectangle(x0_temp,y0_temp,x1_temp,y1_temp,fill=self.color[self.b.next_piece.name_piece.color],outline="white")     
        
    def get_score(self):
        self.text_score.config(state=NORMAL)
        n=int(self.text_score.get("0.0",END))
        self.text_score.config(state=DISABLED)
        return n

    def show_score(self,n):
        self.text_score.config(state=NORMAL)
        self.text_score.delete("0.0",END)
        self.text_score.insert(END,str(n))
        self.text_score.config(state=DISABLED)

    def show_level(self,lvl):
        self.text_level.config(state=NORMAL)
        self.text_level.delete("0.0",END)
        self.text_level.insert(END,str(lvl))
        self.text_level.config(state=DISABLED)

    def show_record(self,record):
        self.text_record.config(state=NORMAL)
        self.text_record.delete("0.0",END)
        self.text_record.insert(END,str(record))
        self.text_record.config(state=DISABLED)
    
        

    def quit(self):
        save_record(max(self.get_score(),get_record()))
        self.fen.quit()
        self.fen.destroy()
        
