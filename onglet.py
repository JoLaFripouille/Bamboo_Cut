import customtkinter as ctk
from tkinter import messagebox
from logic import optimiser_decoupe
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

class OptimisationDecoupeApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        # Le reste de votre code d'initialisation



        # Charger les images pour les boutons
        self.edit_image = ctk.CTkImage(Image.open("images/EDIT.png"), size=(20, 20))
        self.sup_image = ctk.CTkImage(Image.open("images/SUP.png"), size=(20, 20))

        # Frame pour le choix des matériaux
        self.chix_materiaux_frame = ctk.CTkFrame(self, corner_radius=7)
        self.chix_materiaux_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.profil_label = ctk.CTkLabel(self.chix_materiaux_frame, text="Choix du profil acier:")
        self.profil_label.grid(row=0, column=0, padx=5, pady=5)
        self.profil_combobox = ctk.CTkComboBox(self.chix_materiaux_frame, values=["IPE", "HEA", "PLAT", "TUBE CARRE", "TUBE RECTANGULAIRE", "AUTRE"])
        self.profil_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.dimension_label = ctk.CTkLabel(self.chix_materiaux_frame, text="Dimension:")
        self.dimension_label.grid(row=1, column=0, padx=5, pady=5)
        self.dimension_entry = ctk.CTkEntry(self.chix_materiaux_frame)
        self.dimension_entry.grid(row=1, column=1, padx=5, pady=5)


        self.longueur_barre_label = ctk.CTkLabel(self, text="Longueur de la barre:")
        self.longueur_barre_label.grid(row=1, column=0, padx=10, pady=10)
        self.longueur_barre_entry = ctk.CTkEntry(self)
        self.longueur_barre_entry.grid(row=1, column=1, padx=10, pady=10)
        self.longueur_barre_entry.insert(0, "6000")  # Valeur par défaut pour la longueur de la barre

        self.epaisseur_lame_label = ctk.CTkLabel(self, text="Épaisseur de la lame:")
        self.epaisseur_lame_label.grid(row=2, column=0, padx=10, pady=10)
        self.epaisseur_lame_entry = ctk.CTkEntry(self)
        self.epaisseur_lame_entry.grid(row=2, column=1, padx=10, pady=10)
        self.epaisseur_lame_entry.insert(0, "3")  # Valeur par défaut pour l'épaisseur de la lame

        # Nouvelle frame pour les entrées des morceaux
        self.entree_frame = ctk.CTkFrame(self, corner_radius=7)
        self.entree_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Frame scrollable pour afficher les morceaux ajoutés
        self.morceaux_frame = ctk.CTkScrollableFrame(self, width=575, height=400, corner_radius=7)
        self.morceaux_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10)

        self.calculer_button = ctk.CTkButton(self, text="Calculer découpe", command=self.calculer_decoupe)
        self.calculer_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.export_pdf_button = ctk.CTkButton(self, text="Exporter PDF", command=self.generer_pdf)
        self.export_pdf_button.grid(row=5, column=1, padx=10, pady=10)

        # Zone de résultats placée à droite de toutes les autres
        self.result_area = ctk.CTkTextbox(self, width=470, height=700, corner_radius=15)
        self.result_area.grid(row=0, column=3, rowspan=6, padx=10, pady=20)

        self.morceaux_entries = {}
        self.barres_calculees = None
        self.creer_ligne_entree()

    def creer_ligne_entree(self):
        # Placer les entrées dans la nouvelle frame 'entree_frame'
        self.repere_entry = ctk.CTkEntry(self.entree_frame, placeholder_text='Repère', width=60, corner_radius=7)
        self.repere_entry.grid(row=0, column=0, padx=5, pady=5)
        self.longueur_entry = ctk.CTkEntry(self.entree_frame, placeholder_text='Longueur', width=100, corner_radius=7)
        self.longueur_entry.grid(row=0, column=1, padx=5, pady=5)
        self.quantite_entry = ctk.CTkEntry(self.entree_frame, placeholder_text='Quantité', width=100, corner_radius=7)
        self.quantite_entry.grid(row=0, column=2, padx=5, pady=5)
        self.angle1_entry = ctk.CTkEntry(self.entree_frame, placeholder_text='Angle 1', width=60, corner_radius=7)
        self.angle1_entry.grid(row=0, column=3, padx=5, pady=5)
        self.angle2_entry = ctk.CTkEntry(self.entree_frame, placeholder_text='Angle 2', width=60, corner_radius=7)
        self.angle2_entry.grid(row=0, column=4, padx=5, pady=5)
        self.ajouter_morceau_button = ctk.CTkButton(self.entree_frame, text="Ajouter un morceau", command=self.ajouter_morceau, corner_radius=7)
        self.ajouter_morceau_button.grid(row=0, column=5, padx=10, pady=10)
        
    def mettre_a_jour_onglet(self, *_):
        if self.tab_buttons:
            dimension = self.dimension_entry.get().strip()
            profil = self.profil_combobox.get()
            if dimension:
                self.tab_buttons[0].config(text=f"{profil} {dimension}")
            else:
                self.tab_buttons[0].config(text="SANS TITRE")

    def ajouter_onglet(self):
        dimension = self.dimension_entry.get().strip()
        profil = self.profil_combobox.get()
        if dimension:
            tab_text = f"{profil} {dimension}"
        else:
            tab_text = "SANS TITRE"

        new_tab_button = ctk.CTkButton(self.bandeau_frame, text=tab_text, corner_radius=7)
        new_tab_button.grid(row=0, column=len(self.tab_buttons) + 1, padx=5, pady=5)
        self.tab_buttons.append(new_tab_button)
        self.ajouter_onglet_button.grid(row=0, column=len(self.tab_buttons) + 1, padx=5, pady=5)

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

            morceaux_data = {
                'longueur': longueur_morceau,
                'quantite': quantite,
                'angle1': angle1,
                'angle2': angle2
            }
            self.morceaux_entries[repere] = morceaux_data

            # Créer une nouvelle ligne dans morceaux_frame et l'aligner correctement
            row_idx = len(self.morceaux_entries)

            repere_label = ctk.CTkLabel(self.morceaux_frame, text=repere, width=60, corner_radius=7)
            repere_label.grid(row=row_idx, column=0, padx=5, pady=5)
            longueur_label = ctk.CTkLabel(self.morceaux_frame, text=str(longueur_morceau), width=100, corner_radius=7)
            longueur_label.grid(row=row_idx, column=1, padx=5, pady=5)
            quantite_label = ctk.CTkLabel(self.morceaux_frame, text=str(quantite), width=100, corner_radius=7)
            quantite_label.grid(row=row_idx, column=2, padx=5, pady=5)
            angle1_label = ctk.CTkLabel(self.morceaux_frame, text=str(angle1), width=60, corner_radius=7)
            angle1_label.grid(row=row_idx, column=3, padx=5, pady=5)
            angle2_label = ctk.CTkLabel(self.morceaux_frame, text=str(angle2), width=60, corner_radius=7)
            angle2_label.grid(row=row_idx, column=4, padx=5, pady=5)
            
    # Ajouter les boutons Modifier et Supprimer avec les images
            modifier_button = ctk.CTkButton(self.morceaux_frame, text="", image=self.edit_image, fg_color="transparent", width=50, command=lambda r=repere: self.modifier_morceau(r), corner_radius=7)
            modifier_button.grid(row=row_idx, column=5, padx=5, pady=5)
            supprimer_button = ctk.CTkButton(self.morceaux_frame, text="", image=self.sup_image, fg_color="transparent", width=50, command=lambda r=repere: self.retirer_morceau(r), corner_radius=7)
            supprimer_button.grid(row=row_idx, column=6, padx=5, pady=5)

            # Effacer les champs après l'ajout
            self.repere_entry.delete(0, 'end')
            self.longueur_entry.delete(0, 'end')
            self.quantite_entry.delete(0, 'end')
            self.angle1_entry.delete(0, 'end')
            self.angle2_entry.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour tous les champs des morceaux.")
            return

    def retirer_morceau(self, repere):
        row_idx = list(self.morceaux_entries.keys()).index(repere)
        for widget in self.morceaux_frame.grid_slaves(row=row_idx):
            widget.grid_forget()  # Effacer la ligne du morceau
        del self.morceaux_entries[repere]

    def modifier_morceau(self, repere):
        # Remettre les valeurs dans les champs d'entrée pour modification
        data = self.morceaux_entries[repere]
        self.repere_entry.delete(0, 'end')
        self.longueur_entry.delete(0, 'end')
        self.quantite_entry.delete(0, 'end')
        self.angle1_entry.delete(0, 'end')
        self.angle2_entry.delete(0, 'end')

        self.repere_entry.insert(0, repere)
        self.longueur_entry.insert(0, data['longueur'])
        self.quantite_entry.insert(0, data['quantite'])
        self.angle1_entry.insert(0, data['angle1'])
        self.angle2_entry.insert(0, data['angle2'])

        self.retirer_morceau(repere)

    def calculer_decoupe(self):
        try:
            longueur = int(self.longueur_barre_entry.get())
            epaisseur = int(self.epaisseur_lame_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour la longueur de la barre et l'épaisseur de la lame.")
            return

        morceaux_dict = self.morceaux_entries

        nombre_de_barres, barres, chute_totale = optimiser_decoupe(longueur, epaisseur, morceaux_dict)
        self.barres_calculees = barres  # Sauvegarder les données des barres calculées pour le PDF

        self.result_area.delete("1.0", "end")
        self.result_area.insert("end", f'Nombre total de barres nécessaires: {nombre_de_barres}\n')
        for i, barre in enumerate(barres):
            self.result_area.insert("end", f'Barre {i+1}:\n')
            for morceau in barre['morceaux']:
                self.result_area.insert("end", f'  - Repère: {morceau[0]}, Longueur: {morceau[1]},quantite: {morceau[2]}, Angle 1: {morceau[2]}, Angle 2: {morceau[3]}\n')
            self.result_area.insert("end", f'  Longueur de la chute: {barre["chute"]}\n')
        self.result_area.insert("end", f'Longueur totale de la chute: {chute_totale}\n')

    def generer_pdf(self):
        if not self.barres_calculees:
            messagebox.showerror("Erreur", "Aucune découpe n'a été calculée pour générer le PDF.")
            return

        # Créer le document PDF
        doc = SimpleDocTemplate("decoupe_barres.pdf", pagesize=A4)
        elements = []

        # Style pour les paragraphes
        styles = getSampleStyleSheet()
        titre_style = styles['Title']

        # Ajouter un titre
        titre = Paragraph("Fiche de debit", titre_style)
        elements.append(titre)

        for i, barre in enumerate(self.barres_calculees):
            # Ajouter une section pour chaque barre
            section_titre = Paragraph(f"Barre {i+1}:", styles['Heading2'])
            elements.append(section_titre)

            # Créer les données du tableau pour chaque barre sans la colonne 'Quantité'
            data = [['Repère', 'Longueur', 'Angle 1', 'Angle 2']]
            for morceau in barre['morceaux']:
                # Nous n'affichons plus la quantité (on passe de 5 à 4 colonnes)
                if len(morceau) < 4:
                    morceau = list(morceau) + [''] * (4 - len(morceau))  # Compléter avec des valeurs vides
                data.append([morceau[0], morceau[1], morceau[2], morceau[3]])

            # Ajouter la longueur de la chute
            data.append(["", "", "", f"Chute: {barre['chute']}"])

            # Créer le tableau
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

        # Construire le PDF
        doc.build(elements)
        messagebox.showinfo("Succès", "Le fichier PDF a été généré avec succès sous le nom 'decoupe_barres.pdf'.")

