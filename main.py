import customtkinter as ctk
from tkinter import messagebox
from onglet import OptimisationDecoupeApp

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("mise en Barre")
        self.geometry("1400x750+0+0")  # Ajusté pour accueillir le contenu

        # Cadre principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Cadre pour les onglets à gauche
        self.tab_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.tab_frame.pack(side="left", fill="y")

        # Cadre défilable pour contenir les boutons d'onglet et le bouton 'Nouvel onglet'
        self.tabs_container = ctk.CTkScrollableFrame(self.tab_frame)
        self.tabs_container.pack(fill="both", expand=True)

        # Bouton 'Options' (placé après le cadre défilable)
        self.options_button = ctk.CTkButton(self.tab_frame, text="Options", command=self.open_options)
        self.options_button.pack(fill="x", pady=(5, 5))

        # Bouton 'Nouvel onglet' (placé à l'intérieur du tabs_container)
        self.new_tab_button = ctk.CTkButton(self.tabs_container, text="Nouvel onglet", command=self.create_new_tab)
        self.new_tab_button.pack(fill="x", pady=(5, 5))

        # Dictionnaires pour stocker les onglets
        self.tabs = {}
        self.tab_order = []
        self.current_tab = None

        # Cadre de contenu à droite
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Ajouter l'onglet par défaut
        self.add_tab("Sans titre")

    def add_tab(self, tab_name):
        # Créer un cadre pour le bouton d'onglet
        tab_container = ctk.CTkFrame(self.tabs_container, height=30)
        tab_container.pack(fill="x")

        # Configurer le gestionnaire de placement pour le positionnement absolu
        tab_container.pack_propagate(False)

        # Bouton d'onglet
        tab_button = ctk.CTkButton(tab_container, text=tab_name, command=lambda: self.select_tab(tab_name))
        tab_button.place(relwidth=1, relheight=1)  # Occupe tout l'espace du conteneur

        # Bouton de suppression superposé sur le bouton d'onglet
        delete_button = ctk.CTkButton(tab_container, text="X", width=20, height=20, command=lambda: self.delete_tab(tab_name))
        delete_button.place(relx=0.9, rely=0.1)  # Position relative à l'intérieur du conteneur

        # Replacer le bouton 'Nouvel onglet' en bas
        self.new_tab_button.pack_forget()
        self.new_tab_button.pack(fill="x", pady=(5, 5))

        # Stocker les informations de l'onglet
        self.tabs[tab_name] = {
            'frame': tab_container,
            'button': tab_button,
            'delete_button': delete_button,
            'content': OptimisationDecoupeApp(self.content_frame)
        }
        self.tab_order.append(tab_name)

        # Sélectionner le nouvel onglet
        self.select_tab(tab_name)

    def create_new_tab(self):
        tab_name = f"Onglet {len(self.tabs) + 1}"
        self.add_tab(tab_name)

    def select_tab(self, tab_name):
        self.current_tab = tab_name
        # Masquer tous les contenus des onglets
        for tab in self.tabs.values():
            tab['content'].pack_forget()
        # Afficher le contenu de l'onglet sélectionné
        self.tabs[tab_name]['content'].pack(fill="both", expand=True)

    def delete_tab(self, tab_name):
        # Détruire le cadre de l'onglet
        tab_container = self.tabs[tab_name]['frame']
        tab_container.destroy()

        # Détruire le contenu de l'onglet
        tab_content = self.tabs[tab_name]['content']
        tab_content.destroy()

        # Supprimer l'onglet des structures de données
        del self.tabs[tab_name]
        self.tab_order.remove(tab_name)

        # Si l'onglet supprimé est le courant, mettre à jour le contenu
        if self.current_tab == tab_name:
            self.current_tab = None
            # Sélectionner un autre onglet si disponible
            if self.tab_order:
                self.select_tab(self.tab_order[-1])  # Sélectionner le dernier onglet
            else:
                # S'il n'y a plus d'onglets, masquer le content_frame
                for widget in self.content_frame.winfo_children():
                    widget.destroy()

    def open_options(self):
        # Méthode appelée lorsque le bouton 'Options' est cliqué
        messagebox.showinfo("Options", "Les options seront disponibles ici.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
