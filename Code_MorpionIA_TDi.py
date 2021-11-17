# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:39:45 2021

@author: rayan
"""

#%% Codeurs
#Rayan MESSAOUDI
#Romane MOISON
#Annabel MERCERON
#Victor MONNOYEUR

#%%

import time
import numpy as np
import math
from random import randint

# On définit le plateau
class Plateau:    
    def __init__(self,tab=np.array([[None for x in range(12)] for x in range(12)])):
        if (tab.shape!=(12,12)):
            self.tab=np.array([[None for x in range(12)] for x in range(12)])
        else:
            self.tab=tab    
    def __str__(self):
        msg="   1  2  3  4  5  6  7  8  9 10 11 12 \n"
        for i in range(self.tab.shape[0]):
            if (i+1<10):
                msg+=str(i+1)+"  "
            else:
                msg+=str(i+1)+" "
            for j in range(self.tab.shape[1]):
                if self.tab[i][j]==None:
                    msg+="_  "
                else:
                    msg+=str(self.tab[i][j])+"  "
            msg+="\n"
        return msg

    
#%% Méthodes pour jouer


def Action(plateau):
    """On renvoie une liste contenant toutes les positions qui ne sont pas occupées"""
    l = []
    for i in range(plateau.tab.shape[0]):
        for j in range(plateau.tab.shape[1]):	
            if plateau.tab[i][j] == None:
                l.append([i,j])
    return l

def Result(plateau,case,symbolJoueur):
    """actualise le plateau du jeu en ajoutant le pion du joueur en case=[x,y]"""
    x,y=case[0],case[1]    
    plateau.tab[x][y]=symbolJoueur    
    return plateau


def Terminal_Test(plateau):
    """renvoie True si il y a un gagnant, False si il n'y en a pas, None si match nul"""
    # i,j sont les coord du pion qui vient juste d'être posé
    # on vérifie que le plateau n'est pas entièrement rempli
    plateauRempli=False
    presenceGagnant=False
    caseVide=[x[i] for x in plateau.tab for i in range(12) if x[i]==None]
    if len(caseVide)==0:
        plateauRempli=True  

    # on vérifie sur les lignes qu'il n'y ait pas de gagnant
    for i in range(plateau.tab.shape[0]):
        for j in range(plateau.tab.shape[1]-3):
            if(plateau.tab[i][j]==plateau.tab[i][j+1]==plateau.tab[i][j+2]==plateau.tab[i][j+3]!=None):
                presenceGagnant=True

    # on vérifie sur les colonnes qu'il n'y ait pas de gagnant   
    for j in range(plateau.tab.shape[1]):
        for i in range(plateau.tab.shape[0]-3):
            if(plateau.tab[i][j]==plateau.tab[i+1][j]==plateau.tab[i+2][j]==plateau.tab[i+3][j]!=None):
                presenceGagnant=True

    # on vérifie sur les diagonales à pentes positives qu'il n'y ait pas de gagnant
    for x in range(3,plateau.tab.shape[0]):
        for y in range(3,plateau.tab.shape[1]):
            for k in range (4):
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y-3+k>-1 and y-2+k>-1 and y-1+k>-1 and y+k>-1 and y-3+k<12 and y-2+k<12 and y-1+k<12 and y+k<12):
                    if (plateau.tab[x-3+k][y-3+k]==plateau.tab[x-2+k][y-2+k]==plateau.tab[x-1+k][y-1+k]==plateau.tab[x+k][y+k]!=None):
                        presenceGagnant=True
    
    # on vérifie sur les diagonales à pentes négatives qu'il n'y ait pas de gagnant
    for x in range(3,plateau.tab.shape[0]):
        for y in range(plateau.tab.shape[1]-3):
            for k in range (12):
                if (x-3+k>-1 and x-2+k>-1 and x-1+k>-1 and x+k>-1 and x-3+k<12 and x-2+k<12 and x-1+k<12 and x+k<12 and y+3-k>-1 and y+2-k>-1 and y+1-k>-1 and y-k>-1 and y+3-k<12 and y+2-k<12 and y+1-k<12 and y-k<12):
                    if (plateau.tab[x-3+k][y+3-k]==plateau.tab[x-2+k][y+2-k]==plateau.tab[x-1+k][y+1-k]==plateau.tab[x+k][y-k]!=None):                            
                        presenceGagnant=True

    # on affiche match None si il y a un match nul
    return None if plateauRempli==True and presenceGagnant==False else presenceGagnant


def Utility(plateau,symbolJoueur):#n'est utlisé que sur un plateau dont la partie est fini
    """met 0 pour un match nul, 1 si l'IA gagne et -1 si elle perd"""
    resultat=Terminal_Test(plateau)
    score=0
    if (resultat==True and symbolJoueur=="x"):
        score=10
    elif (resultat==True and symbolJoueur=="o"):
        score=-10
    return score


    
#%% Elagage alpha beta

def MaxValue_ab_A(plateau,alpha,beta,profondeur):
    value=-2000
    if profondeur < 10:
        
        if (Terminal_Test(plateau)!=False):
            #print("fin")
            return Utility(plateau,'o')
        for a in heuristique(plateau):
        #for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            #print(profondeur)
            if (value == 10) :
                return value
            value=max(value,MinValue_ab_A(Result(plateau,a,'x'),alpha,beta,profondeur))
            #print(plateau)
            Result(plateau, a,None)
            #print("value: ",value)
            #print("beta: ",beta)
            if value>=beta:
                return value
            alpha=max(alpha,value)
            #print("alpha: ",alpha)
    #print("valeur finale: ",value)
    return value

def MinValue_ab_A(plateau,alpha,beta,profondeur):
    value=2000
    if profondeur < 10:
        
        if (Terminal_Test(plateau)!=False):
            #print("fin")
            return Utility(plateau,'x')
        for a in heuristique(plateau):
        #for a in Action(plateau):
            Result(plateau, a,None)
            profondeur=profondeur+1
            #print(profondeur)
            if (value == -10) :
                return value
            value=min(value,MaxValue_ab_A(Result(plateau,a,'o'),alpha,beta,profondeur))
            #print(plateau)
            Result(plateau, a,None)
            #print("value2: ",value)
            #print("alpha2: ",alpha)
            if value<=alpha:
                return value
            #print("beta2: ",beta)
            beta=min(beta,value)
    #print("valeur finale: ",value)
    return value            


def abSearch_A(plateau):
    for a in heuristique(plateau):
    #for a in Action(plateau):
        # Joue vers le milieu du plateau si on est les premiers à jouer
        if ( len(Action(plateau)) == 12*12 ):
            r1 = randint(3,plateau.tab.shape[0]-4)
            r2 = randint(3,plateau.tab.shape[0]-4)
            return [[r1,r2]]
        else : 
            res=heuristique(plateau)[0]
            value=MaxValue_ab_A(plateau,-2000, 2000,0)
            #print(value)
            #print("action: ",a)
            #print(Utility(Result(plateau, a, 'x'),'x'))
            if value==MinValue_ab_A(Result(plateau,a,'x'),-2000, 2000,0):
            # if value==MaxValue(Result(plateau, a, 'x')):            
                res=a
            #     value=MinValue(Result(plateau,a,'o'))
            #print(Result(plateau, a, 'x'))
            Result(plateau, a, None)  
        return res


#%% Heuristique

#
def heuristique(plateau):
    """ retourne une liste d'action contenant les "meilleurs actions" en premier et les "mauvaises actions" en dernier"""
    compteur = -1
    listeAction = Action(plateau)
    listeNote = [ 0 for x in range (len(Action(plateau))) ]
    
    for a in listeAction :
        compteur += 1
        ai = a[0]
        aj = a[1]

    # Si une action est "évidente, optimal" on l'a renvoie
    # Si la partie se termine en ajoutant une croix, on met l'action en tête de liste et on retourne la listes des actions
    
#%%  On regarde les colonnes ( pour les croix )

        # Extrémités supérieur
        if (ai == 0) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' ):
                listeNote[compteur] += 10000
            
        # Extrémités inférieur
        elif (ai == plateau.tab.shape[0]-1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' ):
                listeNote[compteur] += 10000
    
        # à une case du bord supérieur
        elif (ai == 1) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x'):
                listeNote[compteur] += 10000
    
        # à une case du bord inférieur
        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 10000
            
        # à deux cases du bord supérieur
        elif (ai == 2) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 10000
    
        # à deux cases du bord inférieur
        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 10000
            
        # à trois cases ou plus des bords (inférieur et supérieur)
        else :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'x' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'x'):
                listeNote[compteur] += 10000
            

#%%  On regarde les lignes ( pour les croix )


        # Extrémités gauche
        if (aj == 0) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' ):
                listeNote[compteur] += 10000
            
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' ):
                listeNote[compteur] += 10000
    
        # à une case du bord gauche
        elif (aj == 1) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x'):
                listeNote[compteur] += 10000
    
        # à une case du bord droite
        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 10000
                
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 10000
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 10000
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'x' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'x'):
                listeNote[compteur] += 10000
            
#%%  On regarde les diagonales à pentes négatives ( pour les croix )


        # Extrémités gauche
        if (aj == 0) : 
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            
        # à une case du bord gauche
        elif (aj == 1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai-1][aj-1] == plateau.tab[ai-2][aj-2] == 'x' ):
                    listeNote[compteur] += 10000
   
            
   
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
        # à une case du bord droite
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x'):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] =='x' ):
                    listeNote[compteur] += 10000


#%%  On regarde les diagonales à pentes positives ( pour les croix )


        # Extrémités gauche
        if (aj == 0) : 
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            
        # à une case du bord gauche
        elif (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
   
            
   
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
        # à une case du bord droit
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
    
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
                
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 10000
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] =='x' ):
                    listeNote[compteur] += 10000
   
        # Si la partie se termine en jouant un rond sur une case, on met la case en tête de liste et on retourne la listes des actions
    
#%%  On regarde les colonnes ( pour les ronds )
    

        # Extrémités supérieur
        if (ai == 0) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' ):
                listeNote[compteur] += 5000
            
        # Extrémités inférieur
        elif (ai == plateau.tab.shape[0]-1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' ):
                listeNote[compteur] += 5000
    

        # à une case du bord supérieur
        elif (ai == 1) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o'):
                listeNote[compteur] += 5000
    
        # à une case du bord inférieur
        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 5000
            
        # à deux cases du bord supérieur
        elif (ai == 2) :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 5000
    
        # à deux cases du bord inférieur
        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai+1][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 5000
            
        # à trois cases ou plus des bords (inférieur et supérieur)
        else :
            if ( plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai+3][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == plateau.tab[ai-1][aj] == 'o' or plateau.tab[ai+1][aj] == plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o' or plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == plateau.tab[ai-3][aj] == 'o'):
                listeNote[compteur] += 5000
            

#%%  On regarde les lignes ( pour les ronds )


        # Extrémités gauche
        if (aj == 0) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' ):
                listeNote[compteur] += 5000
            
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' ):
                listeNote[compteur] += 5000
    
    
        # à une case du bord gauche
        elif (aj == 1) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o'):
                listeNote[compteur] += 5000
    
        # à une case du bord droite
        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 5000
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 5000
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj+1] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 5000
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj+3] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == plateau.tab[ai][aj-1] == 'o' or plateau.tab[ai][aj+1] == plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o' or plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == plateau.tab[ai][aj-3] == 'o'):
                listeNote[compteur] += 5000
            
            
#%%  On regarde les diagonales à pentes négatives ( pour les ronds )


        # Extrémités gauche
        if (aj == 0) : 
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à une case du bord gauche
        elif (aj == 1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj+1] == plateau.tab[ai-1][aj-1] == plateau.tab[ai-2][aj-2] == 'o' ):
                    listeNote[compteur] += 5000
   
               
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # à une case du bord droite
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o'):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+1][aj+1]  == plateau.tab[ai+2][aj+2] == plateau.tab[ai+3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000

#%%  On regarde les diagonales à pentes positives ( pour les ronds )


        # Extrémités gauche
        if (aj == 0) : 
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            
        # à une case du bord gauche
        elif (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
   
            
        # Extrémités droite
        elif (aj == plateau.tab.shape[1]-1) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # à une case du bord droit
        elif (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
                
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( ai >= 0 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 5000
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-1):
                if ( plateau.tab[ai-1][aj+1]  == plateau.tab[ai-2][aj+2] == plateau.tab[ai-3][aj+3] == 'o' ):
                    listeNote[compteur] += 5000
    
    
        # On priorise ensuite les actions où l'on gagne en deux tours
    
    
#%%  On regarde les colonnes ( victoire en deux tours )
    
    
        # à une case du bord supérieur
        if (ai == 1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 1000
    
            
        # à deux cases du bord supérieur
        elif (ai == 2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 1000
            
            
            # à une case du bord inférieur
        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 1000
            
    
        # à deux cases du bord inférieur
        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                listeNote[compteur] += 1000
            
        # à trois cases ou plus des bords (inférieur et supérieur)
        else :
            if ( ai != 0 and ai != plateau.tab.shape[0]-1 ):    
                if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'x'):
                    listeNote[compteur] += 1000
            

#%%  On regarde les lignes ( victoire en deux tours )

    
        # à une case du bord gauche
        if (aj == 1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 1000
    
            
        # à deux cases du bord gauche 
        elif (aj == 2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 1000
            
            
        # à une case du bord droit
        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 1000
            
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                listeNote[compteur] += 1000
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                listeNote[compteur] += 1000
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj != 0 and aj != plateau.tab.shape[1]-1 ):         
                if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'x'):
                    listeNote[compteur] += 1000
                if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'x'):
                    listeNote[compteur] += 1000

#%% On regarde les diagonales à pentes négatives ( victoire en deux tours )


        # à une case du bord gauche
        if (aj == 1) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à deux cases du bord gauche
        if (aj == 2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
                
        # à une case du bord droit
        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à deux cases du bord droit
        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'x' ):
                        listeNote[compteur] += 1000
                        ###
                    
#%% On regarde les diagonales à pentes positives ( victoire en deux tours )


        # à une case du bord gauche
        if (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à deux cases du bord gauche
        if (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
                
        # à une case du bord droit
        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à deux cases du bord droit
        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                    listeNote[compteur] += 1000
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                    listeNote[compteur] += 1000
                
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'x' ):
                        listeNote[compteur] += 1000
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'x' ):
                        listeNote[compteur] += 1000
                        

#%%  On regarde les colonnes ( défaite en deux tours )
    
    
        # à une case du bord supérieur
        if (ai == 1) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 500
    
            
        # à deux cases du bord supérieur
        elif (ai == 2) :
            if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 500
            
            
        # à une case du bord inférieur
        elif (ai == plateau.tab.shape[0]-2) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 500
            
    
        # à deux cases du bord inférieur
        elif (ai == plateau.tab.shape[0]-3) :
            if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                listeNote[compteur] += 500
            
        # à trois cases ou plus des bords (inférieur et supérieur)
        else :
            if ( ai != 0 and ai != plateau.tab.shape[0]-1 ):    
                if ( plateau.tab[ai-3][aj] == plateau.tab[ai+1][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai-2][aj] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai-2][aj] == plateau.tab[ai+2][aj] == None and plateau.tab[ai-1][aj] == plateau.tab[ai+1][aj] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai-1][aj] == plateau.tab[ai+3][aj] == None and plateau.tab[ai+1][aj] == plateau.tab[ai+2][aj] == 'o'):
                    listeNote[compteur] += 500
            

#%%  On regarde les lignes ( défaite en deux tours )

    
        # à une case du bord gauche
        if (aj == 1) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 500
    
            
        # à deux cases du bord gauche
        elif (aj == 2) :
            if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 500
            
            
        # à une case du bord droit
        elif (aj == plateau.tab.shape[1]-2) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 500
            
    
        # à deux cases du bord droit
        elif (aj == plateau.tab.shape[1]-3) :
            if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                listeNote[compteur] += 500
            if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                listeNote[compteur] += 500
            
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj != 0 and aj != plateau.tab.shape[1]-1 ):         
                if ( plateau.tab[ai][aj-3] == plateau.tab[ai][aj+1] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj-2] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai][aj-2] == plateau.tab[ai][aj+2] == None and plateau.tab[ai][aj-1] == plateau.tab[ai][aj+1] == 'o'):
                    listeNote[compteur] += 500
                if ( plateau.tab[ai][aj-1] == plateau.tab[ai][aj+3] == None and plateau.tab[ai][aj+1] == plateau.tab[ai][aj+2] == 'o'):
                    listeNote[compteur] += 500

#%% On regarde les diagonales à pentes négatives ( défaite en deux tours )


        # à une case du bord gauche
        if (aj == 1) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
                
        # à deux cases du bord gauche
        if (aj == 2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
                
        # à une case du bord droit
        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à deux cases du bord droit
        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai-3][aj-3] == plateau.tab[ai+1][aj+1] == None and plateau.tab[ai-2][aj-2] == plateau.tab[ai-1][aj-1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai-2][aj-2] == plateau.tab[ai+2][aj+2] == None and plateau.tab[ai-1][aj-1] == plateau.tab[ai+1][aj+1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai-1][aj-1] == plateau.tab[ai+3][aj+3] == None and plateau.tab[ai+1][aj+1] == plateau.tab[ai+2][aj+2] == 'o' ):
                        listeNote[compteur] += 500
                        ###
                    
#%% On regarde les diagonales à pentes positives ( défaite en deux tours )


        # à une case du bord gauche
        if (aj == 1) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
                
        # à deux cases du bord gauche
        if (aj == 2) :
            if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
                
        # à une case du bord droit
        if (aj == plateau.tab.shape[1]-2) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à deux cases du bord droit
        if (aj == plateau.tab.shape[1]-3) :
            if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                    listeNote[compteur] += 500
            if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                    listeNote[compteur] += 500
                
        # à trois cases ou plus des bords (gauche et droit)
        else :
            if ( aj >= 1 and aj <= plateau.tab.shape[1]-2 ):         
                if ( ai >= 1 and ai <= plateau.tab.shape[0]-4):
                    if ( plateau.tab[ai+3][aj-3] == plateau.tab[ai-1][aj+1] == None and plateau.tab[ai+2][aj-2] == plateau.tab[ai+1][aj-1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 2 and aj <= plateau.tab.shape[1]-3 ): 
                if ( ai >= 2 and ai <= plateau.tab.shape[0]-3):
                    if ( plateau.tab[ai+2][aj-2] == plateau.tab[ai-2][aj+2] == None and plateau.tab[ai+1][aj-1] == plateau.tab[ai-1][aj+1] == 'o' ):
                        listeNote[compteur] += 500
            if ( aj >= 3 and aj <= plateau.tab.shape[1]-4 ): 
                if ( ai >= 3 and ai <= plateau.tab.shape[0]-2):
                    if ( plateau.tab[ai+1][aj-1] == plateau.tab[ai-3][aj+3] == None and plateau.tab[ai-1][aj+1] == plateau.tab[ai-2][aj+2] == 'o' ):
                        listeNote[compteur] += 500
                
        # S'il n'y as pas d'action "évidente", on triera la liste des actions en fonction des notes (qu'on zippera a la liste d'action pour les trier a la fin par note) :
    
#%% autres pénalisations
    #On pénalise les actions sur les bords

        if ( ai == 0 or ai == plateau.tab.shape[0]-1):
            listeNote[compteur] -= 0.5
        if ( aj == 0 or aj == plateau.tab.shape[1]-1):
            listeNote[compteur] -= 0.5
    # Si l'action est a une case du bord, on de fait rien

    # On favorise les cases à deux cases du bord
        if ( ai == 2 or ai == plateau.tab.shape[0]-3):
            listeNote[compteur] += 0.25
        if ( aj == 2 or aj == plateau.tab.shape[1]-3):
            listeNote[compteur] += 0.25
            
    # On favorise les cases à trois cases ou plus du bord
    
        if ( ai >= 3 and ai <= plateau.tab.shape[0]-4):
            listeNote[compteur] += 0.5
        if ( aj >= 3 and aj <= plateau.tab.shape[1]-4):
            listeNote[compteur] += 0.5
      
    # La note variera surtout en fonction des cases adjacentes à l'action
    
    
    # On compte le nombre de cases différentes de None autour de l'action, plus il y en a, meilleur sera l'action
    
    # Cas où l'action est à trois cases ou plus du bord
        
        
        #densité
        for k in range (0,8):
            if (ai-3+k>-1 and ai-3+k<8):
                for l in range(0,8):
                    if (aj-3+l>-1 and aj-3+l<8 and math.sqrt((ai-(ai-3+k))**2+(aj-(aj-3+l))**2)!=0):
                        if (plateau.tab[ai-3+k][aj-3+l] != None):
                            listeNote[compteur] += 5/math.sqrt((ai-(ai-3+k))**2+(aj-(aj-3+l))**2)
        listeNote[compteur]/=10                
                        
        #si une case est entourée par deux mêmes pions       
        #en diagonale montante
        if(ai>0 and aj>0 and ai<11 and aj<11 and plateau.tab[ai-1][aj-1]==plateau.tab[ai+1][aj+1]):
            listeNote[compteur]+=1
        #sur la même ligne
        if(aj>0 and aj<11 and plateau.tab[ai][aj-1]==plateau.tab[ai][aj+1]):
            listeNote[compteur]+=1
        #en diagonale descendante
        if(ai<11 and aj>0 and ai>0 and aj<11 and plateau.tab[ai+1][aj-1]==plateau.tab[ai-1][aj+1]):
            listeNote[compteur]+=1
        #sur la même colonne
        if(ai>0 and ai<11 and plateau.tab[ai+1][aj]==plateau.tab[ai-1][aj]):
            listeNote[compteur]+=1
        
        
     
    nStruct = list(zip(listeAction, listeNote))
    nStruct.sort(key = lambda tup : tup[1], reverse = True)
    listeAction = []
    for elem in nStruct:
        listeAction.append(elem[0])
    del listeAction[5:]
    return listeAction


# %% Boucle finale

def Morpion():
    plateau=Plateau()
    debut=input("Voulez vous commencer? (yes/no)")
    if (debut=='yes'):
        tour=1
    else: 
        tour=1
        coup=[5,5]
        plateau=Result(plateau, coup, 'x')
    print("\ni correspond aux lignes, j aux colonnes\n")
    while not Terminal_Test(plateau):    
        print(plateau)
        print("\nTour numéro ",tour)
        
        if(tour%2==0):
            print("(adversaire)")
            temps=time.time()
            symbolJoueur='x'
            
            #on détermine le meilleur coup à jouer grâce à MinMax
            coup=abSearch_A(plateau) #juste pour le test
            print([coup[1]+1,[coup[0]+1]])
            plateau=Result(plateau, coup, symbolJoueur)
            temps=time.time()-temps
            print("\nTemps mis par l'algorithme : ",temps," sec")
            
        else:
            symbolJoueur='o'
            aj=int(input("Veuillez saisir colonne: "))-1
            ai=int(input("Veuillez saisir ligne: "))-1
            while (plateau.tab[ai,aj]!=None or ai==-1 or aj==-1):
                if(ai==-1 or aj==-1):
                    print("ai ou aj ne peuvent pas prendre la valeur 0")
                ai=int(input("Veuillez saisir i: "))-1
                aj=int(input("Veuillez saisir j: "))-1
            coup=[ai,aj] #juste pour le test            
            plateau=Result(plateau, coup, symbolJoueur)
            
        tour+=1
    
    print(plateau)
    if(Terminal_Test(plateau)==None):
        print("Match nul")
    else :
        #méthode afin de déterminer le gagnant : est-ce qu'on modifie Terminal_Test ? Nouvelle méthode ?
        if(tour%2==0): # alors le prochain a joué est 'x' donc celui qui vient de jouer est 'o'
            print('Le joueur avec les pions "o" a gagné')
        else:
            print('Le joueur avec les pions "x" a gagné')
    
Morpion()


# %% TESTS

plateau=Plateau()

plateau.tab=np.array([[None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,'x',None,None,None,None,None,None,None,None,None,None],
                      [None,None,'o',None,None,None,None,None,None,None,None,None],
                      [None,None,'x','o','o','o',None,None,None,None,None,None],
                      [None,None,None,None,'o','x','x',None,None,None,None,None],
                      [None,None,None,None,'x',None,None,None,None,None,None,None],
                      [None,None,None,'x',None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None],
                      [None,None,None,None,None,None,None,None,None,None,None,None]])

#print(Terminal_Test(plateau))
# print(plateau)
