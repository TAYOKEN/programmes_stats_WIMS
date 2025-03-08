import tkinter as tk
from tkinter import messagebox
import numpy as np

def parse_class(classe_str):
    """
    Parse une chaîne représentant une classe au format "[a;b[" et
    retourne un tuple (a, b) sous forme de float.
    """
    if len(classe_str) < 4 or classe_str[0] != "[" or classe_str[-1] != "[":
        raise ValueError(f"Format de classe invalide: {classe_str}\nUtilisez le format [a;b[")
    inner = classe_str[1:-1]
    parts = inner.split(';')
    if len(parts) != 2:
        raise ValueError(f"Format de classe invalide: {classe_str}\nUtilisez le format [a;b[")
    lower = float(parts[0])
    upper = float(parts[1])
    return lower, upper

def calculer_mediane_individuelle(liste, coeffs=None):
    """
    Calcule la médiane pour des données individuelles.
    Si des coefficients sont fournis, la médiane pondérée est calculée
    en reconstituant la série.
    """
    if coeffs:
        valeurs_repliquees = []
        for valeur, coeff in zip(liste, coeffs):
            valeurs_repliquees.extend([valeur] * int(coeff))
        valeurs_repliquees.sort()
        return np.median(valeurs_repliquees)
    else:
        return np.median(sorted(liste))

def calculer_statistiques():
    try:
        # Vérifier si l'utilisateur a renseigné au moins une ligne de données groupées
        classes = []
        effectifs = []
        for row in table_rows:
            classe_val = row[0].get().strip()
            effectif_val = row[1].get().strip()
            if classe_val:  # Si la cellule "Classe" n'est pas vide, on considère la ligne
                classes.append(classe_val)
                if not effectif_val:
                    messagebox.showerror("Erreur", "Veuillez entrer l'effectif correspondant à la classe.")
                    return
                try:
                    effectifs.append(float(effectif_val))
                except ValueError:
                    messagebox.showerror("Erreur", "Effectif invalide dans une ligne de données groupées.")
                    return

        if classes:
            # Mode groupé par classes
            midpoints = []
            widths = []
            lowers = []
            uppers = []
            for classe_str in classes:
                lower, upper = parse_class(classe_str)
                lowers.append(lower)
                uppers.append(upper)
                midpoints.append((lower + upper) / 2)
                widths.append(upper - lower)
            
            total_freq = sum(effectifs)
            if total_freq == 0:
                messagebox.showerror("Erreur", "La somme des effectifs ne peut être zéro.")
                return

            # Moyenne groupée (calculée à partir des points milieux)
            mean = sum(m * f for m, f in zip(midpoints, effectifs)) / total_freq
            # Variance groupée
            variance = sum(f * ((m - mean) ** 2) for m, f in zip(midpoints, effectifs)) / total_freq
            ecart_type = np.sqrt(variance)
            
            # Calcul de la médiane groupée par interpolation
            cum_freq = 0
            mediane = None
            for i, f in enumerate(effectifs):
                prev_cum = cum_freq
                cum_freq += f
                if cum_freq >= total_freq / 2:
                    L = lowers[i]       # borne inférieure de la classe médiane
                    w = widths[i]       # largeur de la classe
                    mediane = L + ((total_freq/2 - prev_cum) / f) * w
                    break

            etendue = uppers[-1] - lowers[0]
            min_val = lowers[0]
            max_val = uppers[-1]

            result_text = (
                "Statistiques pour données groupées par classes :\n"
                f"Moyenne       : {mean:.2f}\n"
                f"Médiane       : {mediane:.2f}\n"
                f"Variance      : {variance:.2f}\n"
                f"Écart-type    : {ecart_type:.2f}\n"
                f"Étendue       : {etendue:.2f}\n"
                f"Min           : {min_val}\n"
                f"Max           : {max_val}"
            )
            result_label.config(text=result_text)
        else:
            # Mode données individuelles
            nombres_str = entree.get().strip()
            if not nombres_str:
                messagebox.showerror("Erreur", "Veuillez entrer des nombres ou remplir le tableau de classes.")
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
                moyenne = sum(x * c for x, c in zip(liste, coeffs)) / somme_coeff
                mediane = calculer_mediane_individuelle(liste, coeffs)
                variance = sum(c * ((x - moyenne) ** 2) for x, c in zip(liste, coeffs)) / somme_coeff
            else:
                moyenne = sum(liste) / len(liste)
                mediane = calculer_mediane_individuelle(liste)
                variance = np.var(liste, ddof=0)
            ecart_type = np.sqrt(variance)
            etendue = max(liste) - min(liste)
            result_text = (
                "Statistiques pour données individuelles :\n"
                f"Moyenne       : {moyenne:.2f}\n"
                f"Médiane       : {mediane:.2f}\n"
                f"Variance      : {variance:.2f}\n"
                f"Écart-type    : {ecart_type:.2f}\n"
                f"Étendue       : {etendue:.2f}\n"
                f"Min           : {min(liste)}\n"
                f"Max           : {max(liste)}"
            )
            result_label.config(text=result_text)
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

def ajouter_ligne():
    """
    Ajoute une nouvelle ligne dans le tableau des données groupées.
    Chaque ligne contient un champ pour la classe et un pour l'effectif.
    """
    global table_rows
    row_index = len(table_rows) + 1  # La ligne 0 est l'en-tête
    classe_entry = tk.Entry(frame_grouped, width=15, font=champ_font, bd=2, relief="groove")
    classe_entry.grid(row=row_index, column=0, padx=5, pady=2)
    effectif_entry = tk.Entry(frame_grouped, width=10, font=champ_font, bd=2, relief="groove")
    effectif_entry.grid(row=row_index, column=1, padx=5, pady=2)
    table_rows.append((classe_entry, effectif_entry))

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Statistiques")
fenetre.geometry("600x700")
fenetre.configure(bg="#f3f4f6")

# Styles
champ_font = ("Helvetica", 12)
label_font = ("Helvetica", 14, "bold")
button_font = ("Helvetica", 12, "bold")

# --- Section pour données individuelles ---
tk.Label(fenetre, text="Données individuelles (optionnel) :", bg="#f3f4f6", font=label_font).pack(pady=(10,0))
tk.Label(fenetre, text="Entrez les nombres séparés par des espaces :", bg="#f3f4f6", font=champ_font).pack(pady=5)
entree = tk.Entry(fenetre, width=40, font=champ_font, bd=2, relief="groove")
entree.pack(pady=5)
tk.Label(fenetre, text="Entrez les coefficients (optionnel) :", bg="#f3f4f6", font=champ_font).pack(pady=5)
entree_coeff = tk.Entry(fenetre, width=40, font=champ_font, bd=2, relief="groove")
entree_coeff.pack(pady=5)

# --- Séparateur ---
tk.Label(fenetre, text="OU", bg="#f3f4f6", font=label_font).pack(pady=10)

# --- Section pour données groupées par classes sous forme de tableau ---
tk.Label(fenetre, text="Données groupées par classes :", bg="#f3f4f6", font=label_font).pack(pady=(10,0))

# Cadre pour le tableau
frame_grouped = tk.Frame(fenetre, bg="#f3f4f6")
frame_grouped.pack(pady=5)

# Ligne d'en-tête du tableau
tk.Label(frame_grouped, text="Classe (ex: [0;5[)", bg="#f3f4f6", font=champ_font).grid(row=0, column=0, padx=5, pady=2)
tk.Label(frame_grouped, text="Effectif", bg="#f3f4f6", font=champ_font).grid(row=0, column=1, padx=5, pady=2)

# Liste qui contiendra les tuples (entrée classe, entrée effectif)
table_rows = []
# Ajout de quelques lignes initiales (ici 3)
for _ in range(3):
    ajouter_ligne()

# Bouton pour ajouter une nouvelle ligne
btn_ajouter_ligne = tk.Button(fenetre, text="Ajouter une ligne", font=button_font,
                              bg="#4CAF50", fg="white", activebackground="#45a049", command=ajouter_ligne)
btn_ajouter_ligne.pack(pady=10)

# Bouton de calcul
btn_calculer = tk.Button(fenetre, text="Calculer", font=button_font,
                         bg="#4CAF50", fg="white", activebackground="#45a049", command=calculer_statistiques)
btn_calculer.pack(pady=20)

# Zone d'affichage du résultat
result_label = tk.Label(fenetre, text="", font=label_font, fg="#333", bg="#f3f4f6")
result_label.pack(pady=10)

# Lancer la boucle principale
fenetre.mainloop()
