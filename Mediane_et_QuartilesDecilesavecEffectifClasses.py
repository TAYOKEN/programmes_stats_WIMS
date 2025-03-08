import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, master):
        self.master = master
        master.title("Calculateur de Médiane, Quartiles et Déciles")

        # Stockage des données : liste de dictionnaires
        self.data = []

        # Création des éléments d'interface
        self.create_widgets()

    def create_widgets(self):
        # Cadre pour la saisie
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        # Saisie des classes
        tk.Label(input_frame, text="Classe (ex: 10-20):").grid(row=0, column=0)
        self.class_entry = tk.Entry(input_frame, width=15)
        self.class_entry.grid(row=0, column=1, padx=5)

        # Saisie des effectifs
        tk.Label(input_frame, text="Effectif:").grid(row=0, column=2)
        self.freq_entry = tk.Entry(input_frame, width=10)
        self.freq_entry.grid(row=0, column=3, padx=5)

        # Bouton d'ajout
        self.add_btn = tk.Button(input_frame, text="Ajouter", command=self.add_class)
        self.add_btn.grid(row=0, column=4, padx=5)

        # Liste des classes
        self.listbox = tk.Listbox(self.master, width=50, height=8)
        self.listbox.pack(pady=5)

        # Bouton de suppression
        self.remove_btn = tk.Button(self.master, text="Supprimer la sélection", command=self.remove_class)
        self.remove_btn.pack(pady=5)

        # Bouton de calcul
        self.calc_btn = tk.Button(self.master, text="Calculer", command=self.calculate)
        self.calc_btn.pack(pady=5)

        # Affichage des résultats
        self.result_label = tk.Label(self.master, text="", justify=tk.LEFT, font=('Arial', 10))
        self.result_label.pack(pady=10)

    def add_class(self):
        # Récupération et validation des entrées
        class_str = self.class_entry.get()
        freq_str = self.freq_entry.get()

        try:
            lower, upper = map(float, class_str.split('-'))
            freq = int(freq_str)
            if freq <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Format invalide!\nClasse: nombre-nombre\nEffectif: entier positif")
            return

        # Vérification de l'ordre des classes
        if self.data and lower < self.data[-1]['upper']:
            messagebox.showerror("Erreur", "Les classes doivent être ordonnées et non chevauchantes")
            return

        # Ajout à la liste
        self.data.append({'lower': lower, 'upper': upper, 'frequency': freq})
        self.listbox.insert(tk.END, f"[{lower}-{upper}] : {freq} effectif(s)")
        
        # Nettoyage des champs
        self.class_entry.delete(0, tk.END)
        self.freq_entry.delete(0, tk.END)

    def remove_class(self):
        # Récupérer l'index de la sélection
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Erreur", "Aucune classe sélectionnée")
            return

        # Supprimer la classe sélectionnée
        index = selection[0]
        self.listbox.delete(index)
        del self.data[index]

    def calculate(self):
        if not self.data:
            messagebox.showerror("Erreur", "Ajoutez des classes avant de calculer")
            return

        # Calcul des effectifs cumulés
        total = sum(classe['frequency'] for classe in self.data)
        positions = [total * p for p in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)]  # Positions des déciles

        # Recherche des classes correspondantes
        def trouver_classe(position):
            cumul = 0
            for classe in self.data:
                cumul += classe['frequency']
                if cumul >= position:
                    return classe
            return self.data[-1]

        # Calcul des déciles
        deciles = {}
        for i, pos in enumerate(positions, start=1):
            deciles[f"D{i}"] = trouver_classe(pos)

        # Calcul des quartiles
        q1_classe = trouver_classe(total * 0.25)
        med_classe = trouver_classe(total * 0.5)
        q3_classe = trouver_classe(total * 0.75)

        # Affichage des résultats
        resultat = (
            f"Classe médiane : [{med_classe['lower']}-{med_classe['upper']}]\n"
            f"Premier quartile (Q1) : [{q1_classe['lower']}-{q1_classe['upper']}]\n"
            f"Troisième quartile (Q3) : [{q3_classe['lower']}-{q3_classe['upper']}]\n\n"
            "Déciles :\n"
        )
        for key, value in deciles.items():
            resultat += f"  {key} : [{value['lower']}-{value['upper']}]\n"

        self.result_label.config(text=resultat)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()