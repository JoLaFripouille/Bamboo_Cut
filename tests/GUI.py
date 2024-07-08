import customtkinter as ctk
from tkinter import messagebox
from main import optimiser_decoupe

# Configurer le thème de customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (par défaut), "Light", "Dark"
ctk.set_default_color_theme("blue")  # Thèmes: "blue" (par défaut), "green", "dark-blue")

class OptimisationDecoupeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Optimisation de découpe de barres")
        self.geometry("800x600")

        self.longueur_barre_label = ctk.CTkLabel(self, text="Longueur de la barre:")
        self.longueur_barre_label.grid(row=0, column=0, padx=10, pady=10)
        self.longueur_barre_entry = ctk.CTkEntry(self)
        self.longueur_barre_entry.grid(row=0, column=1, padx=10, pady=10)

        self.epaisseur_lame_label = ctk.CTkLabel(self, text="Épaisseur de la lame:")
        self.epaisseur_lame_label.grid(row=1, column=0, padx=10, pady=10)
        self.epaisseur_lame_entry = ctk.CTkEntry(self)
        self.epaisseur_lame_entry.grid(row=1, column=1, padx=10, pady=10)

        self.morceaux_frame = ctk.CTkFrame(self)
        self.morceaux_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.ajouter_morceau_button = ctk.CTkButton(self, text="Ajouter un morceau", command=self.ajouter_morceau)
        self.ajouter_morceau_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.calculer_button = ctk.CTkButton(self, text="Calculer découpe", command=self.calculer_decoupe)
        self.calculer_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.result_area = ctk.CTkTextbox(self, width=780, height=300)
        self.result_area.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.morceaux_entries = []
        self.creer_ligne_entree()

    def creer_ligne_entree(self):
        self.repere_entry = ctk.CTkEntry(self.morceaux_frame, placeholder_text='Repère', width=50)
        self.repere_entry.grid(row=len(self.morceaux_entries), column=0, padx=5, pady=5)
        self.longueur_entry = ctk.CTkEntry(self.morceaux_frame, placeholder_text='Longueur', width=100)
        self.longueur_entry.grid(row=len(self.morceaux_entries), column=1, padx=5, pady=5)
        self.quantite_entry = ctk.CTkEntry(self.morceaux_frame, placeholder_text='Quantité', width=100)
        self.quantite_entry.grid(row=len(self.morceaux_entries), column=2, padx=5, pady=5)
        self.angle1_entry = ctk.CTkEntry(self.morceaux_frame, placeholder_text='Angle 1', width=100)
        self.angle1_entry.grid(row=len(self.morceaux_entries), column=3, padx=5, pady=5)
        self.angle2_entry = ctk.CTkEntry(self.morceaux_frame, placeholder_text='Angle 2', width=100)
        self.angle2_entry.grid(row=len(self.morceaux_entries), column=4, padx=5, pady=5)

    def ajouter_morceau(self):
        try:
            repere = self.repere_entry.get()
            longueur_morceau = int(self.longueur_entry.get())
            quantite = int(self.quantite_entry.get())
            angle1 = int(self.angle1_entry.get()) if self.angle1_entry.get() else 0
            angle2 = int(self.angle2_entry.get()) if self.angle2_entry.get() else 0

            if not repere:
                messagebox.showerror("Erreur", "Veuillez entrer un repère pour chaque morceau.")
                return

            morceaux_data = (repere, longueur_morceau, quantite, angle1, angle2)
            self.morceaux_entries.append(morceaux_data)

            row = ctk.CTkFrame(self.morceaux_frame)
            row.grid(row=len(self.morceaux_entries), column=0, columnspan=5, padx=5, pady=5)

            repere_label = ctk.CTkLabel(row, text=repere, width=50)
            repere_label.pack(side="left", padx=5)
            longueur_label = ctk.CTkLabel(row, text=str(longueur_morceau), width=100)
            longueur_label.pack(side="left", padx=5)
            quantite_label = ctk.CTkLabel(row, text=str(quantite), width=100)
            quantite_label.pack(side="left", padx=5)
            angle1_label = ctk.CTkLabel(row, text=str(angle1), width=100)
            angle1_label.pack(side="left", padx=5)
            angle2_label = ctk.CTkLabel(row, text=str(angle2), width=100)
            angle2_label.pack(side="left", padx=5)

            # Ajouter les boutons Modifier et Supprimer
            modifier_button = ctk.CTkButton(row, text="Modifier", command=lambda r=row, d=morceaux_data: self.modifier_morceau(r, d))
            modifier_button.pack(side="left", padx=5)
            supprimer_button = ctk.CTkButton(row, text="Supprimer", command=lambda r=row, d=morceaux_data: self.retirer_morceau(r, d))
            supprimer_button.pack(side="left", padx=5)

            self.repere_entry.delete(0, 'end')
            self.longueur_entry.delete(0, 'end')
            self.quantite_entry.delete(0, 'end')
            self.angle1_entry.delete(0, 'end')
            self.angle2_entry.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour tous les champs des morceaux.")
            return

    def retirer_morceau(self, row, data):
        row.destroy()
        self.morceaux_entries.remove(data)

    def modifier_morceau(self, row, data):
        self.repere_entry.delete(0, 'end')
        self.longueur_entry.delete(0, 'end')
        self.quantite_entry.delete(0, 'end')
        self.angle1_entry.delete(0, 'end')
        self.angle2_entry.delete(0, 'end')

        self.repere_entry.insert(0, data[0])
        self.longueur_entry.insert(0, data[1])
        self.quantite_entry.insert(0, data[2])
        self.angle1_entry.insert(0, data[3])
        self.angle2_entry.insert(0, data[4])

        self.retirer_morceau(row, data)

    def calculer_decoupe(self):
        try:
            longueur = int(self.longueur_barre_entry.get())
            epaisseur = int(self.epaisseur_lame_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour la longueur de la barre et l'épaisseur de la lame.")
            return

        morceaux_dict = {}
        for repere, longueur_morceau, quantite, angle1, angle2 in self.morceaux_entries:
            morceaux_dict[repere] = {
                'longueur': longueur_morceau,
                'quantite': quantite,
                'angle1': angle1,
                'angle2': angle2
            }

        nombre_de_barres, barres, chute_totale = optimiser_decoupe(longueur, epaisseur, morceaux_dict)

        self.result_area.delete("1.0", "end")
        self.result_area.insert("end", f'Nombre total de barres nécessaires: {nombre_de_barres}\n')
        for i, barre in enumerate(barres):
            self.result_area.insert("end", f'Barre {i+1}:\n')
            for morceau in barre['morceaux']:
                self.result_area.insert("end", f'  - Repère: {morceau[0]}, Longueur: {morceau[1]}, Angle 1: {morceau[2]}, Angle 2: {morceau[3]}\n')
            self.result_area.insert("end", f'  Longueur de la chute: {barre["chute"]}\n')
        self.result_area.insert("end", f'Longueur totale de la chute: {chute_totale}\n')

if __name__ == "__main__":
    app = OptimisationDecoupeApp()
    app.mainloop()
