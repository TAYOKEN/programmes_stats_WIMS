import tkinter as tk
from tkinter import messagebox

def calculer_moyenne():
    try:
        liste = [float(x) for x in entree.get().split()]
        moyenne = sum(liste) / len(liste) if liste else 0
        etendue= max(liste) - min(liste)
        result_label.config(text=f"Moyenne : {moyenne:.1f}\n Etendue: {etendue:.1f}\n Min:{min(liste)}\n Max:{max(liste)}")

    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer uniquement des nombres séparés par des espaces.")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Moyenne statistique")
fenetre.geometry("480x270")
fenetre.configure(bg="#f3f4f6")

# Style pour les widgets
champ_font = ("Helvetica", 12)
label_font = ("Helvetica", 14, "bold")
button_font = ("Helvetica", 12, "bold")

# Champ de saisie
tk.Label(fenetre, text="Entrez les nombres séparés par des espaces :", bg="#f3f4f6", font=label_font).pack(pady=10)
entree = tk.Entry(fenetre, width=40, font=champ_font, bd=2, relief="groove")
entree.pack(pady=5)

# Bouton pour calculer la moyenne
btn_calculer = tk.Button(
    fenetre, text="Calculer Moyenne", font=button_font,
    bg="#4CAF50", fg="white", activebackground="#45a049",
    command=calculer_moyenne
)
btn_calculer.pack(pady=15)

# Zone d'affichage du résultat
result_label = tk.Label(fenetre, text="", font=label_font, fg="#333", bg="#f3f4f6")
result_label.pack(pady=10)

# Lancer la boucle principale
fenetre.mainloop()
