

class Board:
    def __init__(self,sizeX,sizeY,piece,next_piece,score):
        '''
            Plateau du jeu

            sizeX : taille horizontale du plateau
            sizeY : taille verticale du plateau
            L : liste du plateau
            piece : piece qui est en cours de placement dans le plateau
            piece_form : raccourci des coordonées des cases de la piece
            tempL : liste d'affichage de L avec la piece
        '''
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.L = self.board(self.sizeX,self.sizeY)
        self.piece = piece
        self.piece_form = piece.name_piece.form
        self.next_piece = next_piece
        self.tempL = self.show_piece(piece) # pour version console
        self.time_sleep=1
        self.score = score
        self.party_proced = True


    def board(self,sizeX,sizeY, val = None):
        ''' creer une liste de taille sizeX par sizeY contenant val partout '''
        l = []
        for i in range(self.sizeY):
            l.append([])
            for j in range(self.sizeX):
                l[i].append(val)
        return l

    def to_line(self,liste):
        ''' affiche en console le plateau du jeu en cours '''
        ch = ""
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                case = liste[i][j]
                if case == None:
                    ch += str('.') + 2*" "
                else:
                    ch += liste[i][j].color[0] + 2*" "
            ch += '\n'
        return ch
    
    # pour utiliser la version console
    def show_piece(self,piece):
        ''' renvoie une copie du plateau de jeu ainsi que la piece en cours de placement placer dans cette copie '''
        l = piece.piece_form()
        tempL = self.copie_liste(self.L)
        for x in l:
            tempL[self.piece.i + x.i][self.piece.j + x.j] = x
        return tempL

    def place_piece(self):
        ''' renvoie la liste du plateau avec toutes les cases de la piece mise sur le plateau '''
        l = self.piece.piece_form()
        for x in l:
            self.L[self.piece.i + x.i][self.piece.j + x.j] = x
        return self.L

    def delete_ligne_complete(self):
        cpt = 0
        for i in range(self.sizeY):
            if self.ligne_complete(i):
                self.L = self.delete_ligne(i)
                cpt += 1
        return self.L,cpt

    def delete_ligne(self,i):
        ''' supprime une ligne i du plateau et en ajoute une à la première ligne '''
        del self.L[i]
        self.L = [[]] + self.L
        for j in range(self.sizeX):
            self.L[0].append(None)
        return self.L

    def ligne_complete(self,i):
        ''' renvoie true si il n'y a aucune case à la ligne i '''
        for j in range(self.sizeX):
            if self.L[i][j] == None:
                return False
        return True

    def copie_liste(self,liste):
        ''' renvoie une capie d'une liste '''
        l = []
        for i in range(len(liste)):
            l.append([])
            for j in range(len(liste[i])):
                l[i].append(liste[i][j])
        return l

    def perdu(self,n):
        ''' renvoie true si la derniere ligne possede au moins une case (à voir pour gerer la derière piece qui n'as pas de place pour se placer et écrases les cases placées...) '''
        for i in range(n):
            for j in range(self.sizeX):
                if self.L[i][j]!=None:
                    return True
        return False

    def down_possible(self):
        ''' renvoie true si pour toutes les coordonnées des cases de la piece elle possède une place en dessous d'elle '''
        l = self.piece.name_piece.form
        for x in l:
            if self.piece.i + x[0] + 1 > self.sizeY - 1 or self.L[self.piece.i + x[0] + 1][self.piece.j + x[1]] != None:
                return False
        return True

    def turn_piece(self):
        L1 = self.piece.name_piece.form
        L2 = self.piece.turn_piece()
        lenX = len(self.L[0])
        decal = 0
        
        for k in range(len(L2)):
            if L2[k][1] + self.piece.j == -1:
                decal = 1
            elif L2[k][1] + self.piece.j == -2:
                decal = 2
            elif L2[k][1] + self.piece.j == lenX:
                decal = -1
            elif L2[k][1] + self.piece.j == lenX+1:
                decal = -2
            if self.piece.i + L2[k][0] in range(len(self.L)) and self.piece.j + L2[k][1] in range(lenX) and self.L[self.piece.i + L2[k][0]][self.piece.j + L2[k][1]] != None:
                if L2[k][1] < 0:
                    decal += 1
                elif L2[k][1] > 0:
                    decal -= 1
                
        if decal != 0:
            self.piece.j += decal
            for x in L2:
                if self.L[x[0]+self.piece.i][self.piece.j+x[1]]!=None:
                    self.piece.j -= decal
                    return L1  
        return L2
                

    def move_possible(self,k):
        l = self.piece.name_piece.form
        for x in l:
            if self.piece.j + x[1] + k < 0 or self.piece.j + x[1] + k > self.sizeX - 1 or self.L[self.piece.i][self.piece.j + x[1] + k] != None:
                return False
        return True
