import tkinter as tk
from tkinter import ttk, messagebox

# Liste qui contiendra les lignes du « tableau » (chaque ligne correspond à une classe)
# Chaque ligne sera un tuple d'Entry : (entrée borne_inf, entrée borne_sup, entrée effectif)
rows = []

def add_row():
    """Ajoute une nouvelle ligne (classe) dans le tableau."""
    row_index = len(rows) + 1  # La première ligne de données est à la ligne 1 (la ligne 0 contient les en-têtes)
    entry_lower = ttk.Entry(table_frame, width=12)
    entry_lower.grid(row=row_index, column=0, padx=5, pady=2)
    entry_upper = ttk.Entry(table_frame, width=12)
    entry_upper.grid(row=row_index, column=1, padx=5, pady=2)
    entry_effectif = ttk.Entry(table_frame, width=12)
    entry_effectif.grid(row=row_index, column=2, padx=5, pady=2)
    rows.append((entry_lower, entry_upper, entry_effectif))

def calculate_median():
    """
    Récupère les données saisies dans le tableau, calcule la médianne
    et affiche les résultats (demi-effectif, classe médiane, rang, amplitude, effectif de la classe et la médianne).
    """
    classes = []  # Liste des tuples (borne_inf, borne_sup, effectif)
    for i, (entry_lower, entry_upper, entry_effectif) in enumerate(rows):
        lower_text = entry_lower.get().strip()
        upper_text = entry_upper.get().strip()
        effectif_text = entry_effectif.get().strip()
        # On ignore les lignes incomplètes
        if lower_text == "" or upper_text == "" or effectif_text == "":
            continue
        try:
            L = float(lower_text)
            U = float(upper_text)
            f = float(effectif_text)
            if U <= L:
                messagebox.showerror("Erreur", f"À la ligne {i+1} : la borne supérieure doit être strictement supérieure à la borne inférieure.")
                return
            if f < 0:
                messagebox.showerror("Erreur", f"À la ligne {i+1} : l'effectif doit être positif.")
                return
            classes.append((L, U, f))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de conversion à la ligne {i+1}. Vérifiez vos saisies.")
            return

    if not classes:
        messagebox.showerror("Erreur", "Veuillez saisir au moins une classe complète (borne inférieure, borne supérieure et effectif).")
        return

    # Calcul du total des effectifs et du demi-effectif
    total_effectif = sum(f for (_, _, f) in classes)
    if total_effectif == 0:
        messagebox.showerror("Erreur", "La somme des effectifs ne peut être nulle.")
        return
    demi_effectif = total_effectif / 2

    # Recherche de la classe médiane
    cumulative = 0
    median_class = None
    cf_before = 0  # cumul des effectifs avant la classe médiane
    for (L, U, f) in classes:
        cf_before = cumulative
        cumulative += f
        if cumulative >= demi_effectif:
            median_class = (L, U, f)
            break

    if median_class is None:
        messagebox.showerror("Erreur", "La classe du demi-effectif n'a pas pu être déterminée.")
        return

    L, U, f = median_class
    amplitude = U - L
    # Rang du demi-effectif dans la classe médiane
    rang = demi_effectif - cf_before
    # Calcul de la médianne selon la formule :
    # Médianne = L + ( (demi_effectif - cumul précédent) / f ) * amplitude
    mediane = L + (rang / f) * amplitude

    # Préparation du texte de résultat
    result_text = f"Demi-effectif : {demi_effectif}\n"
    result_text += f"Classe du demi-effectif : [{L} ; {U}]\n"
    result_text += f"Rang du demi-effectif dans la classe : {rang}\n"
    result_text += f"Amplitude de la classe : {amplitude}\n"
    result_text += f"Effectif de la classe : {f}\n"
    result_text += f"Médianne : {mediane}\n"

    result_label.config(text=result_text)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Calcul de la Médianne (données groupées)")
root.geometry("450x450")

# Création d'un cadre pour le tableau d'entrée
table_frame = ttk.Frame(root, padding="10")
table_frame.pack()

# Ligne d'en-têtes du tableau
header_lower = ttk.Label(table_frame, text="Borne Inférieure", font=("Arial", 10, "bold"))
header_lower.grid(row=0, column=0, padx=5, pady=5)
header_upper = ttk.Label(table_frame, text="Borne Supérieure", font=("Arial", 10, "bold"))
header_upper.grid(row=0, column=1, padx=5, pady=5)
header_effectif = ttk.Label(table_frame, text="Effectif", font=("Arial", 10, "bold"))
header_effectif.grid(row=0, column=2, padx=5, pady=5)

# Ajout de quelques lignes par défaut (ici 5)
for _ in range(5):
    add_row()

# Bouton pour ajouter une nouvelle ligne
button_add_row = ttk.Button(root, text="Ajouter une ligne", command=add_row)
button_add_row.pack(pady=5)

# Bouton pour lancer le calcul de la médianne
button_calculate = ttk.Button(root, text="Calculer la Médianne", command=calculate_median)
button_calculate.pack(pady=5)

# Zone d'affichage des résultats
result_label = ttk.Label(root, text="", padding="10", relief="sunken", anchor="w", justify="left")
result_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
