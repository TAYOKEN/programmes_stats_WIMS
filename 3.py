import tkinter as tk
from tkinter import ttk, messagebox

# Liste qui contiendra les lignes du « tableau »
# Chaque ligne correspond à une classe et est représentée par un tuple d'Entry
rows = []

def add_row():
    """Ajoute une nouvelle ligne (classe) dans le tableau."""
    row_index = len(rows) + 1  # La ligne 0 contient les en-têtes
    entry_lower = ttk.Entry(table_frame, width=12)
    entry_lower.grid(row=row_index, column=0, padx=5, pady=2)
    entry_upper = ttk.Entry(table_frame, width=12)
    entry_upper.grid(row=row_index, column=1, padx=5, pady=2)
    entry_effectif = ttk.Entry(table_frame, width=12)
    entry_effectif.grid(row=row_index, column=2, padx=5, pady=2)
    rows.append((entry_lower, entry_upper, entry_effectif))

def calculate_median():
    """
    Récupère les données saisies dans le tableau, calcule :
      - Le demi-effectif
      - La classe dans laquelle le cumul des effectifs atteint ce demi-effectif
      - Le rang du demi-effectif dans cette classe
      - L'amplitude et l'effectif de la classe
      - La médiane selon la formule pour données groupées
    Puis affiche le tout.
    """
    classes = []  # Liste des classes sous la forme (borne_inf, borne_sup, effectif)
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
                messagebox.showerror("Erreur", f"À la ligne {i+1} : La borne supérieure doit être supérieure à la borne inférieure.")
                return
            if f < 0:
                messagebox.showerror("Erreur", f"À la ligne {i+1} : L'effectif doit être positif.")
                return
            classes.append((L, U, f))
        except Exception:
            messagebox.showerror("Erreur", f"Erreur de conversion à la ligne {i+1}. Vérifiez vos saisies.")
            return

    if not classes:
        messagebox.showerror("Erreur", "Veuillez saisir au moins une classe complète.")
        return

    # Calcul du total des effectifs et du demi-effectif
    total_effectif = sum(f for (_, _, f) in classes)
    demi_effectif = total_effectif / 2

    # Recherche de la classe médiane : celle dans laquelle le cumul des effectifs atteint le demi-effectif
    cumulative = 0
    median_class = None
    cf_before = 0  # cumul des effectifs des classes précédentes
    for (L, U, f) in classes:
        cf_before = cumulative
        cumulative += f
        if cumulative >= demi_effectif:
            median_class = (L, U, f)
            break

    if median_class is None:
        messagebox.showerror("Erreur", "La classe atteignant le demi-effectif n'a pas pu être déterminée.")
        return

    L, U, f = median_class
    amplitude = U - L
    rang = demi_effectif - cf_before  # Le rang du demi-effectif dans la classe médiane
    # Calcul de la médiane pour les données groupées :
    # Médiane = L + ((demi-effectif - cumul des classes précédentes) / effectif de la classe) * amplitude de la classe
    mediane = L + (rang / f) * amplitude

    # Construction de l'affichage des résultats
    result_text = f"Demi-effectif : {demi_effectif}\n"
    result_text += f"Classe du demi-effectif : [{L} ; {U}]\n"
    result_text += f"Rang du demi-effectif dans cette classe : {rang}\n"
    result_text += f"Amplitude de cette classe : {amplitude}\n"
    result_text += f"Effectif de cette classe : {f}\n"
    result_text += f"Que vaut alors la médiane ? {mediane}\n"

    result_label.config(text=result_text)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Calcul de la Médiane (Données Groupées)")
root.geometry("500x500")

# Cadre pour le tableau d'entrée
table_frame = ttk.Frame(root, padding="10")
table_frame.pack()

# Ligne d'en-têtes du tableau
header_lower = ttk.Label(table_frame, text="Borne Inférieure", font=("Arial", 10, "bold"))
header_lower.grid(row=0, column=0, padx=5, pady=5)
header_upper = ttk.Label(table_frame, text="Borne Supérieure", font=("Arial", 10, "bold"))
header_upper.grid(row=0, column=1, padx=5, pady=5)
header_effectif = ttk.Label(table_frame, text="Effectif", font=("Arial", 10, "bold"))
header_effectif.grid(row=0, column=2, padx=5, pady=5)

# Ajout de quelques lignes par défaut (ici 5 lignes)
for _ in range(5):
    add_row()

# Bouton pour ajouter une nouvelle ligne
button_add_row = ttk.Button(root, text="Ajouter une ligne", command=add_row)
button_add_row.pack(pady=5)

# Bouton pour lancer le calcul
button_calculate = ttk.Button(root, text="Calculer la Médiane", command=calculate_median)
button_calculate.pack(pady=5)

# Zone d'affichage des résultats
result_label = ttk.Label(root, text="", padding="10", relief="sunken", anchor="w", justify="left")
result_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
