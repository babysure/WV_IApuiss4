import pygame , numpy as np
from pygame.locals import *
from random import randint
import numpy as np
#import IA_1.py


pygame.init()

largeur = 900
hauteur = 600
fenetre = pygame.display.set_mode((largeur,hauteur))
FPS = 10


# servira a regler l'horloge du jeu
horloge = pygame.time.Clock()


#on génère l'image de fond du jeu
imageFond = pygame.image.load("background2.jpg").convert()
rectFond = imageFond.get_rect()
rectFond.x = 0
rectFond.y = 0




#nb_colone va varié entre 0 et (longueur_tableau - 1)
nb_colone = 0


#on définit les pions
pion_rouge = pygame.image.load("4row_red.png").convert_alpha()
pion_noir = pygame.image.load("4row_black.png").convert_alpha()
pion_jaune = pygame.image.load("4row_yellow.png").convert_alpha() 


#on redimentionne les images
pion_rouge = pygame.transform.scale(pion_rouge,(50,50))
pion_noir = pygame.transform.scale(pion_noir,(50,50))
pion_jaune = pygame.transform.scale(pion_jaune,(50,50))





#on définit les caractéristique du plateau
longueur_tableau = 7
hauteur_tableau = 6

#on définit l'image du carré qui servira à faire le plateau
imagePlateau = pygame.image.load("4row_board.png").convert_alpha()

#on redimentionne la taille de l'image
imagePlateau = pygame.transform.scale(imagePlateau,(60,60))
rectPlateau = imagePlateau.get_rect()

def changer_Joueur(tour_j1):
	tour_j1 = not tour_j1

	return tour_j1


#Partie IA-------------------------------------
def gagner(Tableau):
 
	gagner = False

	#on crée les différentes façon de gagner

	(hauteur_tableau , longueur_tableau) = tableau.shape


	#le code pour gagner verticalement : c'est à dire dans cette direction ( | )  

	for x in range(longueur_tableau):
		for y in range(hauteur_tableau -3):
			if (Tableau[y,x] != 0) and (Tableau[y,x] == Tableau[y+1 ,x]) and (Tableau[y,x] == Tableau[y+2,x]) and (Tableau[y,x] == Tableau[y+3,x]) :
				gagner = True


	#le code pour gagner horizontalement : c'est à dire dans cette direction ( <---> )
	for x in range(longueur_tableau -3):
		for y in range(hauteur_tableau):
			if (Tableau[y,x] != 0) and (Tableau[y,x] == Tableau[y ,x+1]) and (Tableau[y,x] == Tableau[y ,x+2]) and (Tableau[y,x] == Tableau[y,x+3]):
				gagner = True
				


	#le code pour gagner verticalement : c'est à dire dans cette direction (\)
	for x in range(longueur_tableau -3):
		for y in range(hauteur_tableau -3):
			if (Tableau[y,x] != 0) and (Tableau[y,x] == Tableau[y+1 ,x+1]) and (Tableau[y,x] == Tableau[y+2 ,x+2]) and (Tableau[y,x] == Tableau[y+3, x+3]):
				gagner = True
				

	#le code pour gagner verticalement : c'est à dire dans cette direction (/)
	for x in range(longueur_tableau -3):
		for y in range(3,hauteur_tableau):
			if (Tableau[y,x] != 0) and (Tableau[y,x] == Tableau[y-1 ,x-1]) and (Tableau[y,x] == Tableau[y-2, x-2]) and (Tableau[y,x] == Tableau[y-3 ,x-3]) :
				gagner = True


	return gagner



def evalue(plateau, joueur, IA):

	(hauteur_tableau , longueur_tableau) = plateau.shape


    if gagner(plateau) == True :
        if joueur == IA :
            resuVrai = 1
        else :
            resuVrai = -1
    else :

        resuDessous = np.full(plateau.shape , 0)
        resu = -2
        if joueur == IA:
            targetResu  = 1
        else :
            targetResu  = -1

        #on s'est arréter ici


        for choixColone in [0,1,2,3,4,5,6]:

	        plateau[+1 ,choixColone] != 0  and resu != targetResu :
	            # on copie le plateau
	            plateauTemp = [] 
	            for nb in plateau :
	                plateauTemp.append(nb)
	            

	            plateauTemp[choixLigne]-= choixNb

	            resu = evalue(plateauTemp, changerJoueur(joueur),IA)

	            resuDessous.append(resu)                    
        
        if joueur == IA:
            resuVrai = max(resuDessous)
        else :
            resuVrai = min(resuDessous)

        #on récupère l'indices d
    
    #print (plateau, resuVrai, ligneVraie, nbAllVraie)
    return resuVrai

def evalueEtChoisit(plateau):
    bestResult = -2
    choixBestLigne = -1
    choixBestNb = -1

    joueur = 1
    IA = 1

    for choixNb in [1,2,3]:
        for choixLigne in [0,1,2,3]:
            
            if (plateau[choixLigne] - choixNb >= 0) and bestResult < 1 :
                # on copie le plateau
                plateauTemp = [] 
                for nb in plateau :
                    plateauTemp.append(nb)
                

                plateauTemp[choixLigne]-= choixNb
                #print(plateauTemp)

                resu = evalue(plateauTemp, changerJoueur(joueur),IA)
                #print (resu)
                if resu >= bestResult :
                    choixBestLigne = choixLigne
                    choixBestNb = choixNb
                    bestResult = resu
                    #print (bestResult, choixBestLigne, choixBestNb)                    
    
    if (bestResult==1) :
        print("Je gagne")
    else:
        print ("je perds si tu joues bien") 

    return choixBestLigne, choixBestNb


#---------------------------------------------


def Pion(tour_j1):

	if tour_j1 == True :
		pion = pion_rouge

	if tour_j1 == False:
		pion = pion_jaune

	return pion


continuer = 1

gagner = False
tour_j1 = False
pion_x = []
pion_y = []
choix = []
première_partie = True
start = True
tomber = False
chute = 0
#on définit la variable pour la ligne ligne d'arret quand le pion va tomber 
nb_ligne = 0


while continuer :
	touches = pygame.key.get_pressed()
	fenetre.blit(imageFond , rectFond)

	#si on appuie sur "échap" on quite le Jeux

	if touches[K_ESCAPE] :
		continuer = False

	#on génère le plateau à parir de l'image
	for i in range(longueur_tableau):
		for t in range(hauteur_tableau) :
			rectPlateau.x = 250 + (rectPlateau.w)*i
			rectPlateau.y = 230 + (rectPlateau.h)*t 
			fenetre.blit(imagePlateau,rectPlateau)

	if première_partie :

		#choix aléatoire du premier Joueur
		a = randint(0,1)
		if a == 0:
			tour_j1 = False
		else :
			tour_j1 = True
			

		

		#on initialise le tableau numpy

		#ce tableau est initialisr avec des zéros
		Tableau = np.full((hauteur_tableau ,longueur_tableau), 0)

		#on initialise les paramètres 
		pion_x = []
		pion_y = []
		choix = []
		tomber = False
		chute = 0
		gagner = False

		première_partie = False

		start = True


	if start :

		#on permets au pion de ce déplacer
		if tomber == False :
			if touches[K_RIGHT] and (nb_colone >= 0) and (nb_colone < (longueur_tableau -1)):

				nb_colone += 1

			
			if touches[K_LEFT] and (nb_colone > 0) and (nb_colone <= (longueur_tableau -1))  :
				nb_colone -= 1

#------------------------------------------------------------------------------------
			"""
			( on met ce code ici pour ne pas faire des calcules inutiles)
			ici, on définit les règles du jeu 
			"""

			start = False
			première_partie = True
			for y in range(hauteur_tableau):
				for x in range(longueur_tableau):

					#si il y a au moins une case qui n'a pas été remplie
					if Tableau[y][x] == 0 :
						start = True
						première_partie = False


			#on appelle la fonction Gagner
			gagner = gagner(Tableau)


						

		
		 #on affiche le pion qui va tomber

		imageDisque = Pion(tour_j1)
		rectDisque = imageDisque.get_rect()
		rectDisque.x = 255 + nb_colone*60
		rectDisque.y = 150 + chute
		fenetre.blit(imageDisque, rectDisque)

		#on affiche les autres pions
		for k in range(len(choix)) :
				
			imageDisque1 = Pion(choix[k])
			rectDisque1 = imageDisque1.get_rect()
			rectDisque1.x = pion_x[k]
			rectDisque1.y = pion_y[k]
			fenetre.blit(imageDisque1 , rectDisque1)

		
		#on appuie sur la flèche du bas pour faire tomber la pièce
		if (touches[K_DOWN] == True) and (tomber == False) and (Tableau[0][nb_colone] == 0):
			tomber = True
				
			"""
			ce qui ce passe sur le tableau quand la balle tombe:
			si c'est le joueur 1 , la case associer à la place du pion prend la valeur 1
			si c'est le joueur 2 , la case associer à la place du pion prend la valeur -1
			""" 
			for y in range(hauteur_tableau -1):
				if Tableau[y+1 ,nb_colone] != 0 :
					nb_ligne = y
						
					if (tour_j1 == True) :
						Tableau[y ,nb_colone] = 1
						break

					if (tour_j1 == False):
						Tableau[y ,nb_colone] = -1
						break
					

			if Tableau[hauteur_tableau -1 ,nb_colone] == 0 :
				nb_ligne = hauteur_tableau -1

				if tour_j1 == True :
					Tableau[hauteur_tableau -1,nb_colone] = 1

				if tour_j1 == False :
					Tableau[hauteur_tableau -1 ,nb_colone] = -1


		#action à faire si le pion est en train de tomber			

		if tomber == True :

			FPS = 500
			chute += 2

			#si le pion à fini sa chute  
			if rectDisque.y >= (234 + rectPlateau.h*nb_ligne):
				#on ajoute les caractéristique de ce pion dans des listes
				choix.append(tour_j1)
				pion_x.append(rectDisque.x)
				pion_y.append(rectDisque.y)
				
				chute = 0

				tomber = False

				# on écrit cette condition pour savoir qui est le dernier joueur avant la fin de la partie
				if gagner == False:
					#on change de joueur
					tour_j1 = changer_Joueur(tour_j1)
				FPS = 10


	#on limite le nombre de FPS 
	horloge.tick(FPS)

	# rafraichissement de la page 
	pygame.display.flip()

	# parcours de la liste des evenements recus
	 #Si un de ces evenements est de type QUIT

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			continuer = 0
pygame.quit()

"""
on doit associer le plateau à un tableau numpy (array)
ensuite on doit  transformer ce tableau en un vecteur de dimmention 42 (nom_array.flatten() )
ensuite on doit utiliser ce vecteur dans une IA de type deep-Q-learning 
"""

    
"""
pour demain :
il faut faire le geste de la pièce qui tombe dans la fente du plateau (fait) 
il faut mettre le mode switch player-computer 
"""
