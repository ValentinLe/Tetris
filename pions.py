
class Piece:
    def __init__(self,name_piece,i = 1 ,j = 4):
        '''
            name_piece : nom d'une des class du type de la piece (T,Z,Carre,...)
            i : coordonnées verticale du point central de la piece
            j : coordonnées horizontale du point central de la piece
        '''
        self.name_piece = name_piece()
        self.i = i
        self.j = j

    def piece_form(self):
        '''
            renvoie la liste de toutes les cases que contient la piece avec la class Case
        '''
        form = []
        liste = self.name_piece.form
        for x in liste:
            form.append(Case(self.name_piece.color,x[0],x[1]))
        return form

    def turn_piece(self):
        '''
            renvoie les coordonnées sous forme de vecteurs après la rotation des vecteurs de la piece
            
            formule rotation d'un vecteur (x,y) d'un angle phi dans [0,pi] qui donne un veteur (x',y') en multipliant (x,y)
            par la matrice A :

                                A
            [ x' ] = [ cos(phi)  -sin(phi) ] * [ x ]
            [ y' ]   [ sin(phi)   cos(phi) ]   [ y ]

            Dans notre cas phi = -pi/2 pour faire une rotation de 90° vers la droite,
            
            d'où A = [ 0  1 ]
                     [ -1 0 ]
        '''
        l = self.name_piece.form
        L = []
        for x in l:
            L.append((x[1], -x[0]))
        return L



'''
    les types de pieces

    color : couleur de la piece
    form : ensemble des vecteurs pour obtenir les cases adjacentes à partir de la case centrale (le (0,0))

    Par exemple, pour T :

                (-1 , 0)
               
    (0 , -1)    (0 , 0)    (0 , 1)
    
'''

class T(Piece):
    def __init__(self):
        self.color = 'purple'
        self.form = [(0,0),(0,-1),(-1,0),(0,1)]

class Barre(Piece):
    def __init__(self):
        self.color = 'cyan'
        self.form = [(0,0),(0,-1),(0,1),(0,2)]

class Carre(Piece):
    def __init__(self):
        self.color = 'yellow'
        self.form = [(0,0),(-1,0),(0,1),(-1,1)]

class L(Piece):
    def __init__(self):
        self.color = 'orange'
        self.form = [(0,0),(0,-1),(0,1),(-1,1)]

class L_(Piece):
    def __init__(self):
        self.color = 'blue'
        self.form = [(0,0),(0,-1),(-1,-1),(0,1)]

class Z(Piece):
    def __init__(self):
        self.color = 'red'
        self.form = [(0,0),(-1,0),(-1,-1),(0,1)]

class Z_(Piece):
    def __init__(self):
        self.color = 'green'
        self.form = [(0,0),(0,-1),(-1,0),(-1,1)]



class Case:
    def __init__(self,color,i,j):
        ''' 
            color : contient la couleur que la case doit avoir
            i : coordonnées verticale
            j : coordonnées horizontale
        '''
        self.color = color
        self.i = i
        self.j = j


