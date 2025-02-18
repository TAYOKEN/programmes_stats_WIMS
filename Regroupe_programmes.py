import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Définir le dossier contenant les programmes
PROGRAM_FOLDER = "Programmes"

def open_program(filename):
    """
    Ouvre le programme indiqué par 'filename' dans le dossier Programmes.
    Utilisation de os.path pour gérer les chemins.
    """
    path = os.path.abspath(os.path.join(PROGRAM_FOLDER, filename))  # Chemin absolu
    print(f"Chemin construit : {path}")  # Debugging
    print(f"Dossier de travail actuel : {os.getcwd()}")  # Debugging

    # Vérifie que le fichier existe
    if not os.path.exists(path):
        print(f"Erreur : fichier non trouvé -> {path}")  # Debugging
        messagebox.showerror("Erreur", f"Le fichier n'existe pas :\n{path}")
        return

    try:
        # Si c'est un script Python, utiliser l'interpréteur courant
        if path.endswith(".py"):
            subprocess.Popen([sys.executable, path])
        else:
            # Utiliser os.system() pour exécuter le fichier
            os.system(f'"{path}"')  # Windows/Linux compatible
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le programme :\n{e}")

# Définition des chemins pour chaque programme
def open_program1():
    open_program("1.py")

def open_program2():
    open_program("2.py")

def open_program3():
    open_program("3.py")

def open_program4_10():
    open_program("4.py")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu d'ouverture de programmes")
root.geometry("400x200")

# Création d'une barre de menu
menubar = tk.Menu(root)

# Création d'un menu "Programmes"
program_menu = tk.Menu(menubar, tearoff=0)
program_menu.add_command(label="Exercice 1", command=open_program1)
program_menu.add_command(label="Exercice 2", command=open_program2)
program_menu.add_command(label="Exercice 3", command=open_program3)
program_menu.add_command(label="Exercice 4-10", command=open_program4_10)
program_menu.add_separator()
program_menu.add_command(label="Quitter", command=root.quit)

# Ajout du menu "Programmes" à la barre de menu
menubar.add_cascade(label="Feuille 2", menu=program_menu)

# Configuration de la fenêtre pour utiliser cette barre de menu
root.config(menu=menubar)

# Ajout d'un label dans la fenêtre
label = tk.Label(root, text="Utilisez le menu pour ouvrir un programme", font=("Arial", 12))
label.pack(pady=40)

# Lancement de la boucle principale Tkinter
root.mainloop()
