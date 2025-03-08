import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

def format_number(num):
    """Formate un nombre en supprimant les décimales inutiles."""
    formatted = f"{num:.2f}"
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    return formatted

def calculate_median(lst):
    """Calcule la médiane d'une liste de nombres."""
    if not lst:
        return None
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    if n % 2 == 1:
        return sorted_lst[n//2]
    else:
        return (sorted_lst[n//2 -1] + sorted_lst[n//2])/2

def calculate_deciles(sorted_numbers):
    """Calcule les déciles d'une liste de nombres triée."""
    n = len(sorted_numbers)
    deciles = {}
    for i in range(1, 10):
        pos = i * (n + 1) / 10
        lower_idx = int(pos) - 1
        upper_idx = lower_idx + 1
        if lower_idx < 0:
            deciles[f"D{i}"] = sorted_numbers[0]
        elif upper_idx >= n:
            deciles[f"D{i}"] = sorted_numbers[-1]
        else:
            lower_val = sorted_numbers[lower_idx]
            upper_val = sorted_numbers[upper_idx]
            deciles[f"D{i}"] = lower_val + (pos - (lower_idx + 1)) * (upper_val - lower_val)
    return deciles

def calculate_stats():
    """Récupère la saisie, calcule les statistiques et affiche le résultat."""
    input_str = entry_array.get()

    try:
        if ',' in input_str:
            items = [item.strip() for item in input_str.split(',') if item.strip()]
        else:
            items = input_str.split()
        
        numbers = list(map(float, items))
    except Exception as e:
        messagebox.showerror("Erreur", "Veuillez entrer une liste de nombres valide.")
        return
    
    if not numbers:
        messagebox.showerror("Erreur", "La liste ne peut pas être vide.")
        return

    # Calculs de base
    effectif = Counter(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    etendue = max_val - min_val

    # Calcul de la médiane et quartiles
    sorted_numbers = sorted(numbers)
    median = calculate_median(sorted_numbers)
    n = len(sorted_numbers)
    
    if n % 2 == 1:
        lower_half = sorted_numbers[:n//2]
        upper_half = sorted_numbers[n//2 + 1:]
    else:
        lower_half = sorted_numbers[:n//2]
        upper_half = sorted_numbers[n//2:]
    
    q1 = calculate_median(lower_half) if lower_half else median
    q3 = calculate_median(upper_half) if upper_half else median
    iqr = q3 - q1

    # Calcul des déciles
    deciles = calculate_deciles(sorted_numbers)

    # Mode
    max_freq = max(effectif.values())
    modes = [val for val, count in effectif.items() if count == max_freq]

    # Construction du résultat
    result_text = f"Valeur minimale : {format_number(min_val)}\n"
    result_text += f"Valeur maximale : {format_number(max_val)}\n"
    result_text += f"Étendue : {format_number(etendue)}\n"
    result_text += f"Médiane : {format_number(median)}\n"
    result_text += f"Premier quartile (Q1) : {format_number(q1)}\n"
    result_text += f"Troisième quartile (Q3) : {format_number(q3)}\n"
    result_text += f"Intervalle interquartile : {format_number(iqr)}\n\n"

    # Ajout des déciles
    result_text += "Déciles :\n"
    for key, value in deciles.items():
        result_text += f"  {key} : {format_number(value)}\n"
    result_text += "\n"

    # Effectif de chaque valeur
    result_text += "Effectif de chaque valeur :\n"
    for val, count in sorted(effectif.items()):
        result_text += f"  {format_number(val)} : {count}\n"
    
    # Affichage du mode
    if len(modes) == len(effectif):
        result_text += "\nAucun mode (toutes valeurs uniques)"
    elif len(modes) == 1:
        result_text += f"\nMode : {format_number(modes[0])}"
    else:
        modes_str = ", ".join(map(format_number, modes))
        result_text += f"\nModes : {modes_str}"

    # Mise à jour de l'affichage
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result_text)
    text_result.config(state=tk.DISABLED)

# Configuration de l'interface
root = tk.Tk()
root.title("Statistiques avancées")
root.geometry("500x600")

frame_main = ttk.Frame(root, padding=10)
frame_main.pack(fill=tk.BOTH, expand=True)

# Zone de saisie
ttk.Label(frame_main, text="Entrez des nombres séparés par des espaces ou des virgules :").pack()
entry_array = ttk.Entry(frame_main, width=50)
entry_array.pack(pady=5)

# Bouton de calcul
ttk.Button(frame_main, text="Calculer les statistiques", command=calculate_stats).pack(pady=10)

# Zone de résultats avec ascenseur
frame_results = ttk.Frame(frame_main)
frame_results.pack(fill=tk.BOTH, expand=True)

text_result = tk.Text(frame_results, height=20, width=60, state=tk.DISABLED)
scrollbar = ttk.Scrollbar(frame_results, orient=tk.VERTICAL, command=text_result.yview)
text_result.configure(yscrollcommand=scrollbar.set)

text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()