import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

def calculate_stats():
    """
    Récupère la saisie, la convertit en liste de nombres,
    calcule les statistiques et affiche le résultat.
    """
    input_str = entry_array.get()

    # On essaie de convertir la saisie en liste de nombres (float)
    try:
        # Si la chaîne contient une virgule, on suppose que les valeurs sont séparées par des virgules,
        # sinon on utilise les espaces.
        if ',' in input_str:
            items = [item.strip() for item in input_str.split(',') if item.strip()]
        else:
            items = [item for item in input_str.split() if item]
        
        # Conversion en nombres (float)
        numbers = list(map(float, items))
    except Exception as e:
        messagebox.showerror("Erreur", "Veuillez entrer une liste de nombres valide, séparés par des espaces ou des virgules.")
        return
    
    if not numbers:
        messagebox.showerror("Erreur", "La liste ne peut pas être vide.")
        return

    # Calcul des statistiques
    effectif = Counter(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    etendue = max_val - min_val

    # Calcul du/des mode(s)
    max_freq = max(effectif.values())
    modes = [val for val, count in effectif.items() if count == max_freq]

    # Construction du texte de résultat
    result_text = f"Valeur minimale : {min_val}\n"
    result_text += f"Valeur maximale : {max_val}\n"
    result_text += f"Étendue : {etendue}\n\n"
    
    result_text += "Effectif de chaque valeur :\n"
    # On trie les clés pour un affichage ordonné
    for val, count in sorted(effectif.items()):
        result_text += f"  {val} : {count}\n"
    
    # Affichage du ou des mode(s)
    if len(modes) == len(effectif):
        result_text += "\nAucun mode (chaque valeur apparaît le même nombre de fois).\n"
    elif len(modes) == 1:
        result_text += f"\nMode : {modes[0]}\n"
    else:
        modes_str = ", ".join(map(str, modes))
        result_text += f"\nModes : {modes_str}\n"
    
    # Affichage du résultat dans la zone de texte
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result_text)
    text_result.config(state=tk.DISABLED)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Statistiques du tableau")
root.geometry("450x450")  # Taille de la fenêtre

# Création d'un cadre pour un meilleur espacement
frame_input = ttk.Frame(root, padding="10")
frame_input.pack(fill=tk.BOTH, expand=True)

# Instruction pour l'utilisateur
label_instruction = ttk.Label(frame_input, text="Entrez les nombres (séparés par des espaces ou des virgules) :")
label_instruction.pack(pady=5)

# Zone de saisie
entry_array = ttk.Entry(frame_input, width=50)
entry_array.pack(pady=5)

# Bouton pour lancer le calcul
button_calculate = ttk.Button(frame_input, text="Calculer", command=calculate_stats)
button_calculate.pack(pady=10)

# Zone de texte pour afficher les résultats (en lecture seule)
text_result = tk.Text(frame_input, height=15, width=50, state=tk.DISABLED)
text_result.pack(pady=5)

# Boucle principale de l'interface graphique
root.mainloop()
