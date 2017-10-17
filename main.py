
from random import *
import time
from pions import *
from board import *
from interface import *
from threading import Thread
import pickle


def main(fen,b,p):
    #initialisation
    pieces = [T,Barre,Carre,L,L_,Z,Z_]
    speed = 1
    level = 0
    points = [0,40,100,300,1200]
    record = get_record()

    p.show_record(record)
    p.show_score(b.score)
    p.show_level(level)
    
    #debut
    while not(b.perdu(2)) and b.party_proced:
        nb = randint(0,69)%7
        b.piece,b.next_piece = b.next_piece,Piece(pieces[nb])
        p.dessiner_next_piece()
        #deplacement de la piece
        while b.down_possible() and b.party_proced:
            p.grille = b.L
            try:
                p.dessiner_piece()
            except:
                return
            p.cv.update()
            b.piece.i += 1
            time.sleep(b.time_sleep)
        b.L = b.place_piece()
        b.L,cpt = b.delete_ligne_complete()
        p.grille = b.L
        speed *= 0.985
        b.time_sleep = speed
        n = len(b.piece.name_piece.form)
        b.score += level*(10+n) + n + points[cpt]*(level+1)
        p.show_score(b.score)

        level = int(10*(1-speed))
        p.show_level(level)
        if b.score > record:
            record = b.score
            p.show_record(b.score)
        try:
            p.dessiner_grille(b.L)
        except:
            return
    try:
        save_record(max(p.get_score(),get_record()))
        p.dessiner_grille(b.L)
        p.can_move = False
    except:
        return
    save_record(max(p.get_score(),get_record()))

def save_record(record):
    file = 'record.txt'
    try:
        fileR = open(file,'rb')
        n = pickle.load(fileR)
        fileR.close()
    except:
        fileR = open(file,'wb')
        pickle.dump(0,fileR)
        n = 0
        fileR.close()
    if record > n:
        fileW = open(file,'wb')
        pickle.dump(record,fileW)
        fileW.close()
    fileR.close()

def get_record():
    file = "record.txt"
    try:
        fileR = open(file,'rb')
        record = pickle.load(fileR)
        fileR.close()
    except:
        record = 0
    return record


if __name__ == "__main__":
    fen = Tk()
    pieces = [T,Barre,Carre,L,L_]
    b = Board(10,24,Piece(Carre),Piece(choice(pieces)),0)
    p = Interface(fen,b.sizeX,b.sizeY,b)
    mon_thread=Thread(target=main,args=(fen,b,p))
    mon_thread.start()
    fen.mainloop()
