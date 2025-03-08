import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter

def format_number(num):
    """Formate un nombre en supprimant les décimales inutiles."""
    return f"{int(num)}" if num == int(num) else f"{num:.2f}".rstrip('0').rstrip('.') 

def calculate_median(lst):
    """Calcule la médiane d'une liste de nombres."""
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    return (sorted_lst[(n-1)//2] + sorted_lst[n//2])/2 if n % 2 == 0 else sorted_lst[n//2]

def calculate_stats():
    """Traite la saisie des effectifs et calcule les statistiques."""
    input_str = entry_array.get()
    
    try:
        # Découpage des paires valeur:effectif
        pairs = [p.strip() for p in input_str.split(',') if p.strip()]
        numbers = []
        effectif = {}
        
        for pair in pairs:
            if ':' not in pair:
                raise ValueError(f"Format invalide pour : '{pair}'")
            
            valeur_str, effectif_str = pair.split(':', 1)
            valeur = float(valeur_str.strip())
            eff = int(effectif_str.strip())
            
            if eff <= 0:
                raise ValueError(f"Effectif non valide : {eff}")
                
            numbers.extend([valeur] * eff)
            effectif[valeur] = eff  # Stockage des effectifs originaux
            
        if not numbers:
            raise ValueError("Aucune donnée valide entrée")
            
    except Exception as e:
        messagebox.showerror("Erreur", f"Saisie invalide : {str(e)}\nFormat attendu : valeur:effectif,valeur:effectif,...")
        return

    # Calculs statistiques
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    etendue = max_val - min_val
    median = calculate_median(sorted_numbers)
    
    # Calcul des quartiles
    q1 = calculate_median(sorted_numbers[:n//2])
    q3 = calculate_median(sorted_numbers[(n + 1)//2:])
    iqr = q3 - q1

    # Construction des résultats
    result_text = f"Nombre total de données : {n}\n"
    result_text += f"Valeur minimale : {format_number(min_val)}\n"
    result_text += f"Valeur maximale : {format_number(max_val)}\n"
    result_text += f"Étendue : {format_number(etendue)}\n"
    result_text += "-"*40 + "\n"
    result_text += f"Médiane : {format_number(median)}\n"
    result_text += f"Premier quartile (Q1) : {format_number(q1)}\n"
    result_text += f"Troisième quartile (Q3) : {format_number(q3)}\n"
    result_text += f"Intervalle interquartile : {format_number(iqr)}\n"
    result_text += "-"*40 + "\n"
    
    # Affichage des effectifs saisis
    result_text += "Distribution initiale :\n"
    for val, eff in sorted(effectif.items()):
        result_text += f"  {format_number(val)} : {eff} occurrence{'s' if eff > 1 else ''}\n"

    # Mise à jour de l'affichage
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result_text)
    text_result.config(state=tk.DISABLED)

# Interface graphique
root = tk.Tk()
root.title("Statistiques à partir des effectifs")
root.geometry("600x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Entrez les données sous forme valeur:effectif séparés par des virgules :").pack()
entry_array = ttk.Entry(frame, width=50)
entry_array.pack(pady=10)

ttk.Button(frame, text="Calculer", command=calculate_stats).pack()

# Zone de résultats avec ascenseur
text_frame = ttk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

text_result = tk.Text(text_frame, height=15, width=70, wrap=tk.WORD)
scrollbar = ttk.Scrollbar(text_frame, command=text_result.yview)
text_result.configure(yscrollcommand=scrollbar.set)

text_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()