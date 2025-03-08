import tkinter as tk
from tkinter import messagebox
import numpy as np

def calculer_mediane(liste, coeffs):
    """Calcule la médiane d'une série pondérée"""
    valeurs_repliquees = []
    for valeur, coeff in zip(liste, coeffs):
        valeurs_repliquees.extend([valeur] * int(coeff))
    
    valeurs_repliquees.sort()
    return np.median(valeurs_repliquees)

def calculer_variance(liste, coeffs):
    """Calcule la variance (pondérée si coeffs sont fournis)"""
    if coeffs:
        moyenne = sum(x * c for x, c in zip(liste, coeffs)) / sum(coeffs)
        variance = sum(c * (x - moyenne) ** 2 for x, c in zip(liste, coeffs)) / sum(coeffs)
    else:
        variance = np.var(liste, ddof=0)  # Variance non biaisée (population)
    return variance

def calculer_moyenne():
    try:
        nombres_str = entree.get().strip()
        if not nombres_str:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres.")
            return
        liste = [float(x) for x in nombres_str.split()]

        coeffs_str = entree_coeff.get().strip()
        if coeffs_str:
            coeffs = [float(x) for x in coeffs_str.split()]
            if len(coeffs) != len(liste):
                messagebox.showerror("Erreur", "Le nombre de coefficients doit être égal au nombre de nombres.")
                return
            somme_coeff = sum(coeffs)
            if somme_coeff == 0:
                messagebox.showerror("Erreur", "La somme des coefficients ne peut être zéro.")
                return
            # Moyenne pondérée
            moyenne = sum(x * c for x, c in zip(liste, coeffs)) / somme_coeff
            # Médiane pondérée
            mediane = calculer_mediane(liste, coeffs)
            # Variance pondérée
            variance = calculer_variance(liste, coeffs)
        else:
            # Moyenne simple
            moyenne = sum(liste) / len(liste)
            # Médiane simple
            mediane = np.median(sorted(liste))
            # Variance simple
            variance = np.var(liste, ddof=0)

        ecart_type = np.sqrt(variance)
        etendue = max(liste) - min(liste)

        result_label.config(
            text=f"Moyenne : {moyenne:.2f}\n"
                 f"Médiane : {mediane:.2f}\n"
                 f"Variance : {variance:.2f}\n"
                 f"Écart-type : {ecart_type:.2f}\n"
                 f"Étendue : {etendue:.2f}\n"
                 f"Min : {min(liste)}\nMax : {max(liste)}"
        )
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer uniquement des nombres séparés par des espaces.")

# Interface Tkinter
fenetre = tk.Tk()
fenetre.title("Statistiques")
fenetre.geometry("500x450")
fenetre.configure(bg="#f3f4f6")

# Styles
champ_font = ("Helvetica", 12)
label_font = ("Helvetica", 14, "bold")
button_font = ("Helvetica", 12, "bold")

# Entrée des nombres
tk.Label(fenetre, text="Entrez les nombres séparés par des espaces :", bg="#f3f4f6", font=label_font).pack(pady=10)
entree = tk.Entry(fenetre, width=40, font=champ_font, bd=2, relief="groove")
entree.pack(pady=5)

# Entrée des coefficients (optionnel)
tk.Label(fenetre, text="Entrez les coefficients (optionnel) :", bg="#f3f4f6", font=label_font).pack(pady=10)
entree_coeff = tk.Entry(fenetre, width=40, font=champ_font, bd=2, relief="groove")
entree_coeff.pack(pady=5)

# Bouton de calcul
btn_calculer = tk.Button(
    fenetre, text="Calculer", font=button_font,
    bg="#4CAF50", fg="white", activebackground="#45a049",
    command=calculer_moyenne
)
btn_calculer.pack(pady=15)

# Résultats
result_label = tk.Label(fenetre, text="", font=label_font, fg="#333", bg="#f3f4f6")
result_label.pack(pady=10)

# Lancer l'application
fenetre.mainloop()
