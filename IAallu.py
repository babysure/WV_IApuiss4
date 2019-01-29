#on compte toutes les allumette qu'il y a sur sur le plateau 
def compteAllumettes (tab):
	nbAll =0
	for ligne in tab:
		if ligne >= 0:
			nbAll+=ligne
	return nbAll

#on change de joiueur 
def changerJoueur(joueur):
	if  joueur == 1:
		return 2
	return 1



def evalue(plateau, joueur, IA):
	if compteAllumettes(plateau) == 0 :
		if joueur == IA :
			resuVrai = 1
		else :
			resuVrai = -1
	else :

		resuDessous =[]
		resu = -2
		if joueur == IA:
			targetResu  = 1
		else :
			targetResu  = -1

		for choixLigne in [0,1,2,3]:
			for choixNb in [1,2,3]:
				if (plateau[choixLigne] -choixNb >= 0 and resu != targetResu) :
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

allumette = [1,3,5,7]

print (sorted(allumette))
print (allumette)

nextMove = evalueEtChoisit(allumette)
print (nextMove)


""" 
resuVrai = c'est la récompense 
ligneVraie = c'est la ligne ou il faut aller pour réussir 
nbAllVrai = c'est le numéro d'allumette qu'il faut retirer 
""" 