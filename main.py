from ast import Break
import os
import math
from xmlrpc.client import Boolean

("IMPORTANT : pour les mots 'peu importants', nous avons décidé de leur affecter un score tf-idf de None, et non 0. C'est pour cela que dans la définition de la fonction "
"idf, on calcule le logarithme sans ajouter +1.)")
 
def dossier_clean(dossier):
    """Fonction prenant en argument un dossier de fichiers et renvoyant ces fichiers dépourvus de ponctuation et de majuscules.
     -> list"""
    global directory
    directory=os.listdir(dossier)
    Liste_nom_president=[]
    for fichier in directory :
        name=fichier[11:-4] # Permet de prendre uniquement le nom du président dans le titre du fichier
        Liste_nom_president=affichage(name,Liste_nom_president)
        file=open('speeches-20231108/'+ fichier,"r",encoding="utf-8")
        file_clean=open('cleaned/'+fichier[:-4]+"_cleaned.txt","w",encoding='utf-8')
        lignes=file.readlines()
        for line in lignes: # "Nettoie" le fichier de la ponctuation et des majuscules
            file_clean.write(traitement(line))  
        file.close()
        file_clean.close()
    return Liste_nom_president

def traitement(line):
    str=""
    for lettre in line:
        if lettre in ["à","è","é","ô","ù"]:
            str+=lettre
        elif lettre in [".",",",";","?","!",":","-",'"',"`","'"]:
            str+=" "

        else:
            str+=minuscule(lettre)
    return str

def minuscule(lettre:str):
    """Fonction prenant en argument une lettre et renvoyant cette même lettre si c'est une minuscule, ou son équivalent en minuscule si c'est une majuscule."""
    if 65<=ord(lettre)<=90 or 192<=ord(lettre)<=223:
        return chr(ord(lettre)+32)
    else:
        return lettre

def prenom(nom:str):
    """Fonction prenant en argument le nom d'un président et renvoyant ce dernier sans le chiffre qui le suit
        -> str"""
    if nom[-1] in ["0","1","2","3","4","5","6","7","8","9"]:
            nom = nom[:-1]
    return Prenom_president[nom],nom



def affichage(nom : str,liste : list):
    """Fonction prenant en argument le nom d'un président et une liste, puis ajoute dans cette liste le prénom et le nom du président
       -> list"""
    surname,nom=prenom(nom)
    denomination=surname+" "+nom
    if denomination not in liste:
        liste.append(denomination)
    return liste



def fréquence(phrase : str, dico : dict):
    """Fonction prenant en argument une phrase et un entier, et remplissant le nombre d'occurences des mots présents dans la phrase dans la liste globale liste_TF"""
    for mot in phrase.split() :
        if mot in dico.keys():
            dico[mot]+=1
        else :
            dico[mot]=1
    return dico



def idf(mot):
    """Fonction prenant en argument un mot et un entier, calcule son score idf et l'ajoute au dictionnaire global IDF"""
    somme=0
    for l in range(len(clean_directory)):
        if mot in liste_TF[l].keys():
            somme+=1
    IDF[mot] = round(math.log(len(directory)/somme),5)

def TF_IDF(dossier):
    """Fonction prenant en argument un dossier de fichiers et renvoyant une matrice dans laquelle est présent le mot et son score tf idf selon le document
       -> list"""
    M_TF_IDF=[]
    for i in range(len(dossier)): #Cette double boucle permet de calculer le nombre d'occurences de chaque mot dans chaque document
        with open('cleaned/'+dossier[i],"r",encoding='utf-8') as f:
            lignes = f.readlines()
            for e in lignes :
                liste_TF[i]=fréquence(e,liste_TF[i])
    for l in range(len(dossier)): #Cette double boucle permet de calculer le score idf de chaque mot
        for k in liste_TF[l].keys():
            idf(k)
    for mot in IDF.keys(): # Ces boucles imbriquées permettent de créer une matrice et de lui ajouter chaque mot, ainsi que son score tf-idf
        L=[]
        for i in range(len(directory)):
            if mot in liste_TF[i].keys():
                L.append(liste_TF[i][mot]*IDF[mot])
            else:
                L.append(None)
        M_TF_IDF.append(L)
    return M_TF_IDF

def mots_peu_importants(matrice):
    """Fonction prenant en argument une matrice et renvoyant les mots dont la moyenne des scores tf-idf est inférieure à 0,5
    -> list"""
    Liste_mot=[]
    for i in range(len(matrice)): #Parcourt les différents lignes(soit les mots) de la matrice en argument
        moy=0
        occ=0
        for j in range(len(clean_directory)): #Parcourt les différents score d'un mot et fait la moyenne de ces scores ne comptant pas les scores nuls ici None
            if matrice[i][j]!=None:
                moy+=matrice[i][j]
                occ+=1
        moy/=occ
        if moy<=0.5: #Les mots non importants sont ici les mots dont la moyenne de leurs scores est inférieure à 0.5
            mots=list(IDF.keys())
            mot=mots[i]
            Liste_mot.append(mot)
    return Liste_mot

def mots_importants(matrice):
    """Fonction prenant en argument une matrice et renvoyant les mots dont la moyenne des scores tf-idf est supérieure à 1
    -> list"""
    Liste_mot=[]
    for i in range(len(matrice)): #Parcourt les différents lignes(soit les mots) de la matrice en argument
        moy=0
        occ=0
        for j in range(len(clean_directory)): #Parcourt les différents score d'un mot et fait la moyenne de ces scores ne comptant pas les scores nuls ici None
            if matrice[i][j]!=None:
                moy+=matrice[i][j]
                occ+=1
        moy/=occ
        if moy>=4.2: #Les mots importants sont ici les mots dont la moyenne de leurs scores est supérieure à 4.2
            mots=list(IDF.keys())
            mot=mots[i]
            Liste_mot.append(mot)
    return Liste_mot

def mot_repetes_par_Chirac(matrice):
    """Fonction prenant en argument une matrice et renvoyant les mots répétés par Chirac ayant un score tf-idf inférieur à 0,2
    -> list"""
    Liste_mots=list(IDF.keys())
    Liste_mots_repetes=[]
    for i in range(len(matrice)): #On ajoute tous les mots peu importants prononcés par Chirac à une liste
        if matrice[i][0]!=None and matrice[i][0]<=0.5:
            Liste_mots_repetes.append(Liste_mots[i])
        elif matrice[i][1]!=None and matrice[i][1]<=0.5:
            if Liste_mots[i] not in Liste_mots_repetes:
                Liste_mots_repetes.append(Liste_mots[i])
    return Liste_mots_repetes

def president_parle_Nation(matrice):
    """Fonction prenant en argument une matrice, la parcourant et renvoyant le nom des présidents ayant prononcé
       le mot "nation" ainsi que le nom de celui qui l'a plus répété.
       -> list, str"""
    liste_mots=list(IDF.keys())
    liste_président=[]
    president_qui_a_plus_de_nation=""
    indice_nation=0
    for i in range(len(liste_mots)): #On trouve l'endroit où se trouve le mot 'nation' dans la liste des mots.
        if liste_mots[i]=="nation":
            indice_nation=i
            break
    max=matrice[indice_nation][0]
    for j in range(len(matrice[indice_nation])): #On parcourt la matrice à l'indice obtenu précédemment
        if matrice[indice_nation][j] != None: #On donne le nom du président qui a prononcé le mot
            name=directory[j][11:-4]
            name=prenom(name)
            name=name[0]+" "+name[1]
            if name not in liste_président :
                liste_président.append(name)
            if matrice[indice_nation][j]<max :
                max=matrice[indice_nation][j]
                president_qui_a_plus_de_nation=liste_président[-1]
    return liste_président,president_qui_a_plus_de_nation

def president_ecologie(matrice:list,liste_années:list,liste_nom:list):
    """Fonction renvoyant le nom du premier président qui a parlé d'écologie et/ou de climat, ainsi que l'année associée.
       -> str"""
    Liste_apparition_ecologie=[] #Liste pour stocker les indices des textes où le mot climat apparaît
    liste_clés=list(IDF.keys())
    indice_climat=None
    indice_ecologie=None
    if "climat" in liste_clés:
        indice_climat=liste_clés.index("climat")
    if "écologie" in liste_clés:
        indice_ecologie=liste_clés.index("écologie")
    for i in range(len(directory)): #Parcours des textes
        if indice_climat!=None and matrice[indice_climat][i]!=None:
            Liste_apparition_ecologie.append(i)
        if indice_ecologie!=None and matrice[indice_ecologie][i]!=None:
            Liste_apparition_ecologie.append(i)
    indice_min_annee=Liste_apparition_ecologie[0]
    for indice in Liste_apparition_ecologie: #Recherche de l'indice de l'année associée à la première mention du climat
        if liste_années[indice]<liste_années[indice_min_annee]:
            indice_min_annee=indice
    return "C'est " + liste_nom[indice_min_annee] + " en " + str(liste_années[indice_min_annee])

def mots_evoques_par_tous(matrice:list):
    """Fonction parcourant une matrice et renvoyant tous les mots ayant un score tf-idf différent de None, les mots présents dans tous les textes """
    Liste_cles=list(IDF.keys())
    Liste_mot_evoques=[]
    for i in range(len(matrice)):
        booleen=True
        for score in matrice[i]:
            if score==None:
                booleen=False
        if booleen: #Si le mot a un score non nul, on l'ajoute à la liste renvoyée
            Liste_mot_evoques.append(Liste_cles[i])
    return Liste_mot_evoques

def Tokenisation(question):
    """Fonction séparant les mots de la question donnée et les retournant sous forme de liste
       -> list"""
    mots_question = []
    for mot in question.split():
        mots_question.append(mot)
    return mots_question

def recherche_corpus(question):
    """Fonction qui cherche les mots de la question qui sont dans le corpus de documents
       -> list"""
    mot_corpus=[]
    dossier = "cleaned"
    fichiers = os.listdir(dossier)
    for fichier in fichiers :
        with open(dossier+"/"+fichier, "r", encoding="utf-8") as f:
            lignes = f.readlines()
            for ligne in lignes :
                for mot in question:
                     if mot in ligne and mot not in mot_corpus:
                         mot_corpus.append(mot)
    return mot_corpus


def vecteur_TF_IDF_question(question):
    """Fonction qui calcule le score TF-IDF de chaque mot de la question et renvoie le tout dans une liste
       -> list"""
    # Utilisation de la variable globale pour stocker le dictionnaire TF-IDF de la question
    global D_question_tfidf

    # Initialisation du dictionnaire TF-IDF de la question
    D_question_tfidf = {}
    matrice_question = []
    question = str(traitement(question))
    mots_questions = Tokenisation(question)
    intersection = recherche_corpus(mots_questions)
    TF_question = {}
    TF_question = fréquence(question, TF_question)
    Liste_clés = list(IDF.keys())

    # Parcours des clés IDF pour construire le vecteur TF-IDF de la question
    for i in range(len(Liste_clés)):
        mot = Liste_clés[i]
        if mot in intersection:
            score_tfidf = TF_question[mot] * IDF[mot]
            matrice_question.append(score_tfidf)
            D_question_tfidf[mot] = score_tfidf
        else:
            matrice_question.append(0)

    return matrice_question

def transposée(matrice):
    """Fonction calculant la transposée d'une matrice
       -> list"""
    T_matrice=[[matrice[i][j] for i in range(len(matrice))] for j in range (len(matrice[0]))]
    return T_matrice

def prod_scalaire(vecteurA,vecteurB):
    """Fonction calculant le produit scalaire de deux vecteurs
       -> float"""
    prod_sc=0
    for i in range(len(vecteurA)):
        if vecteurA[i]!=None and vecteurB[i]!=None:
            prod_sc+=round(vecteurA[i]*vecteurB[i],3)
    return prod_sc

def norme(vecteur):
    """Fonction calculant la norme d'un vecteur
       -> float"""
    norme=0
    for score in vecteur:
        if score!=None:
            norme+=score**2
    norme=round(math.sqrt(norme),3)
    return norme

def similarité(vecteurA,vecteurB):
    """Fonction calculant la similarité de deux vecteurs
       -> float"""
    normeA=norme(vecteurA)
    normeB=norme(vecteurB)
    prod_sc=prod_scalaire(vecteurA,vecteurB)
    simi=prod_sc/(normeA+normeB)
    return simi

           
def clean_vers_normale(fichier):
    """Fonction qui renvoie le fichier de départ par rapport au fichier traité. """
    return fichier[:-12]+fichier[-4:]



def meilleur_doc(matrice_TF_IDF, matrice_question, dossier):
    """Fonction renvoyant le document le plus pertinent par rapport à la question posée
       -> str"""
    # Transposer la matrice TF-IDF
    matrice_TF_IDF = transposée(matrice_TF_IDF)

    # Liste pour stocker les similarités entre chaque document et la question
    L_simi = []

    # Calculer la similarité entre chaque document et la question
    for ligne in matrice_TF_IDF:
        L_simi.append(similarité(ligne, matrice_question))

    # Initialisation des variables pour le document le plus similaire
    max_similarite = L_simi[0]
    indice_max_similarite = 0

    # Trouver le document avec la similarité maximale
    for i in range(1, len(L_simi)):
        if L_simi[i] > max_similarite:
            max_similarite = L_simi[i]
            indice_max_similarite = i

    nom_document = dossier[indice_max_similarite]
    nom_document = clean_vers_normale(nom_document)

    return nom_document


def réponse(question):
    """Fonction construisant une réponse 'intelligible', qui apporte des informations quant à la question posée par l'utilisateur"""
    # Calcul du vecteur TF-IDF de la question
    vec_tf_idf_qst = vecteur_TF_IDF_question(question)

    # Recherche du terme le plus significatif dans le vecteur TF-IDF de la question
    maxi = 0
    mots_maxis = ""
    for i in range(len(vec_tf_idf_qst)):
        if vec_tf_idf_qst[i] > maxi:
            maxi = vec_tf_idf_qst[i]
    for clé, valeur in D_question_tfidf.items():
        if valeur == maxi:
            mots_maxis = clé
            break

    # Obtention du document le plus pertinent
    doc_pertinent = meilleur_doc(Matrice_TF_IDF, vec_tf_idf_qst, clean_directory)

    reponse = ""

    # Ouverture du document pertinent
    with open("speeches-20231108/" + doc_pertinent, "r", encoding="UTF-8") as doc:
        # Itération sur chaque ligne du document
        for ligne in doc:
            # Division de la ligne en phrases
            phrases = ligne.split(".")

            # Recherche du terme le plus significatif dans chaque phrase
            for phrase in phrases:
                if mots_maxis in phrase:
                    reponse = phrase
                    break

            # Si la réponse est trouvée, sortir de la boucle externe également
            if reponse:
                break

    # Renvoi de la première phrase du document contenant le terme le plus significatif
    return reponse




global Prenom_president
Prenom_president = {"Chirac":"Jacques","Mitterrand":"François","Macron":"Emmanuel",
     "Giscard dEstaing":"Valéry","Hollande":"François","Sarkozy":"Nicolas"}
global clean_directory
clean_directory=os.listdir(r'cleaned')
global liste_TF
liste_TF=[{},{},{},{},{},{},{},{}]
global IDF
IDF = {}
Liste_nom_fichier=['Jacques Chirac','Jacques Chirac', 'Valéry Giscard dEstaing', 'François Hollande', 'Emmanuel Macron', 'François Mitterrand', 'Nicolas Sarkozy']
Liste_années_textes=[1995,2002,1974,2012,2017,1981,1988,2007]
Liste_nom_president=dossier_clean("speeches-20231108")
Matrice_TF_IDF=TF_IDF(clean_directory)




