from tkinter import *
from random import *
from pathlib import Path


base_path = Path(__file__).parent
file_path = base_path / r"Hangman_background.png"

alphabet = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z"

liste_de_mots = ["parallelepipede", "if" , "poumon ", "escrime", "moyen", "gant","saumon","la", "absolutisation", "pirates","couettes","fouiller","neflier","hanche","trompette","argente","alcalinisation","tablettes","cuneiformes","lettres", "manuscrits","orphelin","pays","transatlantique","roucouler","oeuf","navette","kiwi","opposition","savoir","Colonisation","pan","accomplissement","si","doliprane","savon","canneton","regulation","assister","tremblement","canard","chausette","catapulte","bouclier","voisin","acide","louer","tourner","mouche","valoir","sociabiliser","myrtille","danois","wagon","xylophone","zebrer","olivier","urticaire","galoper","polir","chat","sceau","pot","dot","rein","pain","timbre","loup","cou","boucle","rat","eau", "electronegatif","feu","vent","palir","rabougri","tarlouze","pont","pompe","chapeau","loupe","charlotte","diversification","ambulancier","assistant","chapelure","hiboux","gosier","rose","casquette","jaguar","jauge","goule","rateau","pipeau","grimoir","renard","encombrement","accouplement","articulation","charpentier","mourir","entonnoir","miroirs","trompette","kiwi","ordinateurs", "abarticulaire", "peuplements", "horripilation", "capilotractée"]

liste_de_mots.sort(key=len)
liste_mots_en_nb = []

liste_scores = []
Lscore_label = []

for i in range (len(liste_de_mots)):
    liste_mots_en_nb += [len(liste_de_mots[i])]

liste_longueurs = list(set(liste_mots_en_nb))

tentatives = 7
lettres = ''

########################################SETUP################################################################### MERIEN

fenetre = Tk()
fenetre.title("Le jeu du pendu")
fenetre.geometry("750x500")
fenetre.config(bg='gray10')

lenght_entry = Entry(fenetre, width=15, bg='gray40', fg='antiquewhite')

for i in range (3):
    fenetre.columnconfigure(i, weight=1)


image_path = PhotoImage(file=file_path)
bg_img = Label(fenetre, image=image_path)
bg_img.place(relheight=1, relwidth=1)

Label(fenetre, text="Bienvenue sur le jeu du Pendu !", bg='gray10', fg='aquamarine2').grid(column=1,row=0)
Label(fenetre, text="Séléctionnez la longueur du mot :", bg='gray10', fg='aquamarine2').grid(row=1, column=1)


root = Tk()
root.title("Partie en cours...")
root.withdraw()
A=(100, 115)
B=(100, 75)


cnv                 = Canvas(root,width=200, height=200, bg='ivory')
lettres_essayées    = Label(root, text="lettres essayées : " + str(lettres))
aff_mot             = Label(root)
win                 = Label(root, text="Bravo, vous avez gagné !", bg='gainsboro')
essayer             = Button(root, text="Essayer")
guess_entry         = Entry(root, bd=5)
aff_score           = Label(root, text="Votre score : " + str(tentatives))


cvn_list=[
(95,50,110,76), # tête
(A,B), # corps
(B,90,120), # bras gauche
(B,109,120), # bras droit
(A,95,170), # jambe gauche
(A,105,170) # jambe droite
]

################################ FONCTIONS ####################################################################### ANTOINE
def exited_game():
    root.withdraw()
    fenetre.deiconify()


def nombre_de_mots (nombre):
    return liste_mots_en_nb.count(nombre)


def positions_in_list (longueur):
    if longueur  not in liste_mots_en_nb:
        print("Error, no word of this lenght in the list")
        return 0,0
    else :
        position_debut = 0
        for i in range (longueur):
            position_debut += nombre_de_mots(i)
        position_fin = position_debut + nombre_de_mots(longueur) - 1
        return position_debut, position_fin

 ############################################# FENETRE D AIDE ################################################### RAPHAEL

def clicked_help():
    regles = """
    Règles du jeu du Pendu :
    
    Voici comment jouer au pendu :
    1.Entrez la longueur du mot souhaité
    2.Devinez le mot choisit aléatoirement en propossant des lettres
    3.Vous possédez 7 chances de devniez le mot
    4.Chaque lettre incorrecte réduit le nombre d'essaies restants et fait apparaitre sur le dessin un membre de notre cher BOB
    5.Lorsque vous avez devinez toutes les lettres, vous avez gagné
    6.Vous pouvez relancer autant de partie que vous le souhaitez
    7.Bon Jeu !
    """
    rules_window = Tk()
    rules_window.title("Règles du jeu du Pendu")
    Label(rules_window, text=regles, justify=LEFT).grid(row=0, column=0)
    Button(rules_window, text="Ok ! J'ai compris.", command=rules_window.destroy, bg='gainsboro').grid(row=1, column=0)
    rules_window.mainloop()


################################################# AFFICHE DOUBLONS LORS DU DEBUT DE PARTIE ######################### ANTOINE

def double_lettres (element, aflist):

    if solution.count(element) > 1:
        for i in range (len(solution)-1):
            if element in solution[i:]:
                aflist[solution.index(element,i)] = element
                i = solution.index(element,i)
                affichage = aflist

    else :
        affichage = solution[0]+(len(solution)-1)*'*'
    
    return affichage

####################################### SETUP #################################################################### ALEXIS

def setup_game():
    global lettres, tentatives

    guess_entry.grid(column=0, row=3, columnspan=2)
    essayer.grid(column=0, row=4, padx=1, columnspan=2, sticky=NSEW)
    fenetre.withdraw()
    root.deiconify()

    loss.grid_forget()
    win.grid_forget()
    guess_entry.grid(column=0, row=3, columnspan=2)
    essayer.grid(column=0, row=4, padx=1, columnspan=2, sticky=NSEW)

    lettres_essayées.config(text="Lettres essayées : ")
    tentatives = 7
    lettres = ''

    aff_score.config(text="Votre score : " + str(tentatives))
    cnv.delete("all")
    canvas_setup()


def canvas_setup():
    cnv.create_rectangle(100,35,57,185,outline ="black", width=5)
    cnv.create_line(100,52,100,185,fill='ivory', width=5)
    cnv.create_line(57,50,67,35, width=5)
    cnv.create_line(33,185,123,185, width=5)


#######################################  FENETRE DES SCORES ########################################################################## MERIEN

def create():
    txt_score = ''
    scoresW = Toplevel(fenetre)
    scoresW.title("")
    if len(liste_scores)==0:
        txt_score = "Aucun score enregistré pour le moment"
    else :
        for i in range (len(liste_scores)):
            Lscore_label.append("partie n°" + str(i+1) + ': ' + str(liste_scores[i]))
        txt_score = '\n'.join(Lscore_label)
        
    Label(scoresW, text=txt_score).pack()

###################################### WIN-LOOSE SCREEN ########################################################################### ALEXIS


def winner():
    global aff_mot
    liste_scores.append(tentatives)
    essayer.grid_forget()
    guess_entry.grid_forget()         
    win.grid(column=0, row=3, columnspan=2, rowspan=2, sticky=NSEW)
    aff_mot.config(text=solution.upper())



def looser():
    liste_scores.append('0')
    essayer.grid_forget()
    guess_entry.grid_forget()
    loss.grid(column=0, row=3, columnspan=2, rowspan=2, sticky=NSEW)
    aff_mot.config(text=(solution.upper()))

    cnv.delete("all")
    cnv.create_oval(50,50,150,150, fill='Lightpink2', width=5)
    A = 100, 120
    cnv.create_line(A,80,135, width=5)
    cnv.create_line(A,120,135, width=5)
    #oeil gauche
    cnv.create_line(73,78,87,92, width=5)
    cnv.create_line(73,92,87,78, width=5)
    #oeil droit
    cnv.create_line(113,78,127,92, width=5)
    cnv.create_line(113,92,127,78, width=5)


################################################ JEU EN LUI MEME ################################################################# ANTOINE
def clicked_Play_button():
    lenght = lenght_entry.get()
    global affichage, solution, tentatives, lettres, aflist_submit

    setup_game()


    if lenght:
        longueur = int(lenght)
        if longueur not in liste_mots_en_nb:
            print("longueur invalide")
            print("(Randomly selected lenght)", "longueur == ", longueur)
            longueur = randint(len(liste_de_mots[0]),len(liste_de_mots[-1]))
    else :
        longueur = randint(len(liste_de_mots[0]),len(liste_de_mots[-1]))
        print("(Randomly selected lenght)", "longueur == ", longueur)

    global position1, position2
    position1, position2 = positions_in_list(longueur)
    if position1 == 0 and position2 == 0 :
        position1, position2 = positions_in_list(longueur)


    solution = liste_de_mots[randint(position1, position2)].upper()

    affichage = solution[0] + (len(solution)-1) * '*'
    aflist_play = list(affichage)
    aflist_submit = list(affichage)

    aff_mot.config(text=affichage)
       
    tentatives = 7

    affichage = double_lettres(solution[0], aflist_play)

    aff_mot.config(text=" ".join(aflist_play))

################################################################################################################# ALEXIS

    def submit_guess ():
        global essayer, guess_entry, lettres, liste_scores
        global aflist_submit, affichage, solution, tentatives
        lettres_essayées.config(text="Lettres essayées : " + str(lettres))

        aflist_submit = list(affichage)

        guess = (guess_entry.get()).upper()
        if len(guess) > 1 or len(guess) == 0 or guess not in alphabet:
            if guess == solution :
                guess_entry.delete(0,'end')
                winner()
            elif len(guess) == len(solution) and guess != solution:
                looser()
                guess_entry.delete(0,'end')
            else:
                root.title("Veuillez ne tester qu'une lettre ")
                root.after(2000, lambda: root.title("Partie en cours..."))
                guess_entry.delete(0,'end')

        else :
            guess_entry.delete(0,'end')
            if affichage != solution :
                if guess not in lettres and guess not in aflist_submit :
                    if guess in solution :

                        if solution.count(guess) == 1 :
                            aflist_submit[solution.index(guess)] = guess
                            affichage = aflist_submit
                            aff_mot.config(text=" ".join(aflist_submit))
                        else:
                            affichage = double_lettres(guess, aflist_submit)
                            aff_mot.config(text=" ".join(aflist_submit))

                    else :
                        lettres = guess + " " + lettres
                        lettres_essayées.config(text="Lettres essayées : " + str(lettres))
                        tentatives = tentatives - 1
                        aff_score.config(text = "Votre score : " + str(tentatives))
                        if tentatives == 6 :
                            cnv.create_oval(cvn_list[6-tentatives],fill='Lightpink2', width=5)
                        elif 0 < tentatives < 6 :
                            cnv.create_line(cvn_list[6-tentatives], width=5)
                        elif tentatives == 0 :
                            looser ()

        if aflist_submit.count("*") == 0 :
            winner()

    essayer.config(command=submit_guess)
    essayer.grid(column=0, row=4, padx=1, columnspan=2, sticky=NSEW)

################################################################################################################# ALEXIS 

def recharge_word ():
    global affichage, tentatives, solution, lettres
    setup_game()

    SBefore = solution
    while solution == SBefore :
        solution = liste_de_mots[randint(position1, position2)].upper()

    affichage = solution[0] + (len(solution)-1) * '*'
    aff_mot.config(text=' '.join(affichage))
    aflist_recharge= list(affichage)

    affichage = double_lettres(solution[0], aflist_recharge)
    
    aff_mot.config(text=" ".join(aflist_recharge))




################################################################################################################# MERIEN


loss = Label(root, text=("Vous avez perdu :(") , bg='gainsboro')
Button(root, text="Quitter",command=exited_game).grid(column=3, row=3, padx=1, rowspan=2, sticky=NSEW)
Button(root, text="Recharger le mot", command=recharge_word).grid(column=2, row=3, padx=1, rowspan=2, sticky=NSEW)

Button(fenetre, text="Scores", bg='gray40', fg='antiquewhite', command=create).grid(column=0, row=0, sticky=NSEW)
Button(fenetre, text="Aide", bg='gray40', fg='antiquewhite' ,command=clicked_help).grid(column=2, row=0, sticky=NSEW)
Button(fenetre,width=10, height=5, text ='jouer',bg='gray40', fg='antiquewhite', command=clicked_Play_button).grid(column=0,row=3)
Button(fenetre,width=10, height=5, text ='quitter',bg='gray40', fg='antiquewhite', command=exit).grid(column=2,row=3)
lenght_entry = Entry(fenetre, width=15, bg='gray40', fg='antiquewhite')


aff_score.grid(column=2, row=0, columnspan=2)
aff_mot.grid(column=0, row=1, padx=1, rowspan=2, columnspan=2, sticky=NSEW)
lenght_entry.grid(column=1,row=2)
guess_entry.grid(column=0, row=3, columnspan=2)
cnv.grid(column = 2, row = 1, rowspan=2, columnspan=2)
lettres_essayées.grid(column=0, row=0, columnspan=2)


fenetre.mainloop()