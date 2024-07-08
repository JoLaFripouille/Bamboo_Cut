import customtkinter as ctk
from tkinter import messagebox
from main import optimiser_decoupe

# Configurer le thème de customtkinter
ctk.set_appearance_mode("System")  # Modes: "System" (par défaut), "Light", "Dark"
ctk.set_default_color_theme("blue")  # Thèmes: "blue" (par défaut), "green", "dark-blue"


class OptimisationDecoupeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bamboo Cut")
        self.geometry("800x600")
        self.main_color = "#1E1C23"
        self.entry_color = "#34303C"
        self.btn_color = "#131118"
        self.configure(fg_color=self.main_color)

        self.longueur_barre_label = ctk.CTkLabel(self, text="Longueur de la barre:")
        self.longueur_barre_label.grid(row=0, column=0, padx=10, pady=10)
        self.longueur_barre_entry = ctk.CTkEntry(
            self, fg_color=self.entry_color, corner_radius=10
        )
        self.longueur_barre_entry.grid(row=0, column=1, padx=10, pady=10)

        self.epaisseur_lame_label = ctk.CTkLabel(self, text="Épaisseur de la lame:")
        self.epaisseur_lame_label.grid(row=1, column=0, padx=10, pady=10)
        self.epaisseur_lame_entry = ctk.CTkEntry(
            self, fg_color=self.entry_color, corner_radius=10
        )
        self.epaisseur_lame_entry.grid(row=1, column=1, padx=10, pady=10)

        self.morceaux_frame = ctk.CTkFrame(
            self, height=5, bg_color=self.main_color, fg_color=self.main_color
        )
        self.morceaux_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.ajouter_morceau_button = ctk.CTkButton(
            self,
            height=60,
            text="Ajouter un morceau",
            command=self.ajouter_morceau,
            fg_color=self.btn_color,
            border_width=2,
        )
        self.ajouter_morceau_button.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10
        )

        self.calculer_button = ctk.CTkButton(
            self,
            height=60,
            text="Calculer découpe",
            command=self.calculer_decoupe,
            fg_color=self.btn_color,
            border_width=2,
        )
        self.calculer_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_area = ctk.CTkTextbox(self, width=780, height=300)
        self.result_area.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.morceaux_entries = []

    def ajouter_morceau(self):
        row = ctk.CTkFrame(
            self.morceaux_frame, fg_color=self.main_color, bg_color=self.main_color
        )
        row.pack(fill="x", pady=5)

        repere_entry = ctk.CTkEntry(
            row, width=50, height=30, fg_color=self.entry_color, corner_radius=10
        )
        repere_entry.pack(side="left", padx=5)
        longueur_entry = ctk.CTkEntry(
            row, width=100, height=30, fg_color=self.entry_color, corner_radius=10
        )
        longueur_entry.pack(side="left", padx=5)
        quantite_entry = ctk.CTkEntry(
            row, width=100, height=30, fg_color=self.entry_color, corner_radius=10
        )
        quantite_entry.pack(side="left", padx=5)
        angle1_entry = ctk.CTkEntry(
            row, width=100, height=30, fg_color=self.entry_color, corner_radius=10
        )
        angle1_entry.pack(side="left", padx=5)
        angle2_entry = ctk.CTkEntry(
            row, width=100, height=30, fg_color=self.entry_color, corner_radius=10
        )
        angle2_entry.pack(side="left", padx=5)
        supprimer_button = ctk.CTkButton(
            row, text="Supprimer", command=lambda r=row: self.retirer_morceau(r)
        )
        supprimer_button.pack(side="left", padx=5)

        self.morceaux_entries.append(
            (repere_entry, longueur_entry, quantite_entry, angle1_entry, angle2_entry)
        )

    def retirer_morceau(self, row):
        row.destroy()
        self.morceaux_entries = [
            entry for entry in self.morceaux_entries if entry[0].master != row
        ]

    def calculer_decoupe(self):
        try:
            longueur = int(self.longueur_barre_entry.get())
            epaisseur = int(self.epaisseur_lame_entry.get())
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Veuillez entrer des valeurs valides pour la longueur de la barre et l'épaisseur de la lame.",
            )
            return

        morceaux_dict = {}
        for (
            repere_entry,
            longueur_entry,
            quantite_entry,
            angle1_entry,
            angle2_entry,
        ) in self.morceaux_entries:
            try:
                repere = repere_entry.get()
                longueur_morceau = int(longueur_entry.get())
                quantite = int(quantite_entry.get())
                angle1 = int(angle1_entry.get()) if angle1_entry.get() else 0
                angle2 = int(angle2_entry.get()) if angle2_entry.get() else 0

                if not repere:
                    messagebox.showerror(
                        "Erreur", "Veuillez entrer un repère pour chaque morceau."
                    )
                    return

                morceaux_dict[repere] = {
                    "longueur": longueur_morceau,
                    "quantite": quantite,
                    "angle1": angle1,
                    "angle2": angle2,
                }
            except ValueError:
                messagebox.showerror(
                    "Erreur",
                    "Veuillez entrer des valeurs valides pour tous les champs des morceaux.",
                )
                return

        nombre_de_barres, barres, chute_totale = optimiser_decoupe(
            longueur, epaisseur, morceaux_dict
        )

        self.result_area.delete("1.0", "end")
        self.result_area.insert(
            "end", f"Nombre total de barres nécessaires: {nombre_de_barres}\n"
        )
        for i, barre in enumerate(barres):
            self.result_area.insert("end", f"Barre {i+1}:\n")
            for morceau in barre["morceaux"]:
                self.result_area.insert(
                    "end",
                    f"  - Repère: {morceau[0]}, Longueur: {morceau[1]}, Angle 1: {morceau[2]}, Angle 2: {morceau[3]}\n",
                )
            self.result_area.insert(
                "end", f'  Longueur de la chute: {barre["chute"]}\n'
            )
        self.result_area.insert("end", f"Longueur totale de la chute: {chute_totale}\n")


if __name__ == "__main__":
    app = OptimisationDecoupeApp()
    app.mainloop()
