import os
import random
import time

# ANSI escape codes pour les couleurs
RESET = "\033[0m"
VERT_FLASH = "\033[1;32m"  # Vert flash pour la case active
ROUGE = "\033[0;31m"  # Rouge pour les chiffres pré-insérés
VERT_LIGNE = "\033[0;32m"  # Vert pour les lignes de séparation
VERT_PROGRESS = "\033[0;32m"  # Vert pour la barre de progression

# Fonction pour nettoyer l'affichage du terminal
def effacer_terminal():
    os.system('clear')  # Pour Linux/Mac
    # os.system('cls')  # Pour Windows, si tu es sur Windows

# Fonction d'affichage de la grille avec des couleurs pour les chiffres pré-insérés et les lignes
def afficher_grille(grille, grille_initiale, surbrillance=None):
    effacer_terminal()
    for ligne in range(9):
        if ligne % 3 == 0 and ligne != 0:
            print(VERT_LIGNE + "-" * 21 + RESET)  # Ligne verte horizontale
        for colonne in range(9):
            valeur = grille[ligne][colonne]
            if grille_initiale[ligne][colonne] != 0:
                # Chiffres pré-insérés en rouge
                print(ROUGE + str(valeur) + RESET, end=" ")
            elif surbrillance == (ligne, colonne):
                # Case active en vert flash
                print(VERT_FLASH + str(valeur) + RESET, end=" ")
            else:
                print(str(valeur) + " ", end="")
            
            # Lignes verticales en vert entre les blocs 3x3
            if colonne % 3 == 2 and colonne != 8:
                print(VERT_LIGNE + "| " + RESET, end="")
        print()

# Fonction pour calculer et afficher la barre de progression
def afficher_barre_progression(grille, tentatives):
    total_cases = 81
    cases_remplies = sum(1 for ligne in grille for case in ligne if case != 0)
    progression = cases_remplies / total_cases
    taille_barre = 20  # Nombre de caractères pour la barre de progression

    # Construire la barre de progression
    remplissage = int(progression * taille_barre)
    barre = VERT_PROGRESS + '█' * remplissage + RESET + ' ' * (taille_barre - remplissage)
    pourcentage = int(progression * 100)

    # Afficher la barre de progression et le pourcentage
    print(f"Progression: [{barre}] {pourcentage}%")
    print(f"Tentatives: {tentatives}")

# Fonction brute-force (backtracking) pour résoudre la grille pas à pas
def est_valide(grille, num, pos):
    # Vérifie si le numéro est valide dans la ligne
    for i in range(9):
        if grille[pos[0]][i] == num and pos[1] != i:
            return False
    # Vérifie la colonne
    for i in range(9):
        if grille[i][pos[1]] == num and pos[0] != i:
            return False
    # Vérifie le carré 3x3
    carre_x = pos[1] // 3
    carre_y = pos[0] // 3
    for i in range(carre_y * 3, carre_y * 3 + 3):
        for j in range(carre_x * 3, carre_x * 3 + 3):
            if grille[i][j] == num and (i, j) != pos:
                return False
    return True

def trouver_case_vide(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                return (i, j)  # Ligne, Colonne
    return None

# Fonction de résolution avec visualisation des étapes et barre de progression
def resoudre_sudoku(grille, grille_initiale, tentatives):
    case_vide = trouver_case_vide(grille)
    if not case_vide:
        return True  # Sudoku résolu
    else:
        ligne, colonne = case_vide

    for i in range(1, 10):
        tentatives[0] += 1  # Compter la tentative pour chaque nombre essayé
        if est_valide(grille, i, (ligne, colonne)):
            grille[ligne][colonne] = i
            # Afficher la grille avec la case en cours
            afficher_grille(grille, grille_initiale, (ligne, colonne))
            afficher_barre_progression(grille, tentatives[0])
            time.sleep(0.01)  # Pause rapide (0.01s)

            if resoudre_sudoku(grille, grille_initiale, tentatives):
                return True

            # Réinitialiser la case si ça ne fonctionne pas
            grille[ligne][colonne] = 0
            afficher_grille(grille, grille_initiale, (ligne, colonne))
            afficher_barre_progression(grille, tentatives[0])
            time.sleep(0.01)  # Pause rapide (0.01s)

    return False

# Générateur de valeurs pour chaque carré 3x3, avec validation des lignes et colonnes
def pre_remplir_carres(grille):
    for carre_y in range(3):
        for carre_x in range(3):
            # Créer un ensemble de valeurs uniques
            valeurs = random.sample(range(1, 10), 4)  # Choisir 4 nombres uniques entre 1 et 9
            # On va essayer de remplir ces 4 valeurs dans le carré de 3x3
            cases = [(i, j) for i in range(carre_y * 3, carre_y * 3 + 3)
                     for j in range(carre_x * 3, carre_x * 3 + 3)]
            random.shuffle(cases)  # Mélanger les cases pour une distribution aléatoire

            for val in valeurs:
                for i in range(len(cases)):
                    case = cases[i]
                    if est_valide(grille, val, case):
                        grille[case[0]][case[1]] = val
                        break  # Sortir dès qu'on a placé la valeur

# Boucle principale
if __name__ == "__main__":
    # Créer une grille vide
    grille = [[0] * 9 for _ in range(9)]
    
    # Pré-remplir chaque carré 3x3 avec 4 valeurs aléatoires valides
    pre_remplir_carres(grille)
    
    # Copier la grille initiale pour afficher les chiffres pré-insérés en rouge
    grille_initiale = [ligne[:] for ligne in grille]

    print("Grille générée aléatoirement avec 4 valeurs dans chaque carré 3x3 :")
    afficher_grille(grille, grille_initiale)
    input("Appuyez sur Entrée pour résoudre...")

    # Initialiser le compteur de tentatives
    tentatives = [0]  # Utiliser une liste pour pouvoir modifier la valeur à l'intérieur de la fonction
    # Résolution du Sudoku avec visualisation
    resoudre_sudoku(grille, grille_initiale, tentatives)
    print("\nGrille résolue :")
    afficher_grille(grille, grille_initiale)
    afficher_barre_progression(grille, tentatives[0])  # Afficher la barre finale
