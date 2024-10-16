import customtkinter as ctk
from tkinter import messagebox
from onglet import OptimisationDecoupeApp
from time import sleep

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

        # Cadre pour contenir les onglets et le bouton 'Nouvel onglet'
        self.tabs_container = ctk.CTkFrame(self.tab_frame)
        self.tabs_container.pack(fill="both", expand=True)

        # Liste pour stocker les informations des onglets
        self.tabs = {}
        self.tab_order = []
        self.current_tab = None

        # Bouton 'Options' (placé après le cadre des onglets)
        self.options_button = ctk.CTkButton(
            self.tab_frame,
            text="Options",
            command=self.open_options
        )
        self.options_button.pack(fill="x", pady=(5, 5))

        # Bouton 'Nouvel onglet' (placé dans tabs_container)
        self.new_tab_button = ctk.CTkButton(
            self.tabs_container,
            text="Nouvel onglet",
            command=self.create_new_tab,
            width=200,
            height=30
        )
        # Positionner le bouton 'Nouvel onglet' en haut initialement
        self.new_tab_button.place(x=0, y=0)

        # Cadre de contenu à droite
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Ajouter l'onglet par défaut
        self.add_tab("Sans titre", animate=False)

    def create_new_tab(self):
        # Étape 1 : Animer le bouton 'Nouvel onglet' pour le faire descendre
        self.animate_new_tab_button_down(self.add_new_tab_without_animation)

    def animate_new_tab_button_down(self, callback):
        steps = 10
        delta = 35 / steps

        def animate(step):
            if step < steps:
                new_tab_button_y = self.new_tab_button.winfo_y()
                new_y = new_tab_button_y + delta
                self.new_tab_button.place_configure(y=new_y)
                self.tabs_container.update()
                
                self.after(10, lambda: animate(step + 1))
            else:
                # Une fois l'animation terminée, appeler la fonction de rappel
                callback()
        animate(0)

    def add_new_tab_without_animation(self):
        # Obtenir la position où le bouton 'Nouvel onglet' se trouvait avant de descendre

        y_position = self.new_tab_button.winfo_y() - 35  # Hauteur du bouton

        # Ajouter le nouvel onglet à la position précédente du bouton 'Nouvel onglet'
        self.add_tab(y_position=y_position, animate=False)

    def add_tab(self, tab_name=None, y_position=None, animate=True):
        if tab_name is None:
            tab_name = f"Onglet {len(self.tabs) + 1}"

        if y_position is None:
            y_position = len(self.tab_order) * 35

        # Créer le nouvel onglet à la position spécifiée
        tab_container = ctk.CTkFrame(
            self.tabs_container,
            width=200,
            height=30
        )
        tab_container.place(x=0, y=y_position)
        tab_container.pack_propagate(False)

        # Bouton d'onglet
        tab_button = ctk.CTkButton(
            tab_container,
            text=tab_name,
            command=lambda: self.select_tab(tab_name),
            width=200,
            height=30
        )
        tab_button.place(relwidth=1, relheight=1)

        # Bouton de suppression superposé sur le bouton d'onglet
        delete_button = ctk.CTkButton(
            tab_container,
            text="X",
            width=20,
            height=20,
            command=lambda: self.delete_tab(tab_name)
        )
        delete_button.place(relx=0.9, rely=0.1)

        # Insérer l'onglet dans la liste
        self.tab_order.append(tab_name)
        self.tabs[tab_name] = {
            'container': tab_container,
            'button': tab_button,
            'delete_button': delete_button,
            'content': OptimisationDecoupeApp(self.content_frame),
            'y_position': y_position
        }

        # Mettre à jour les positions
        self.update_tab_positions()

        # Sélectionner le nouvel onglet
        self.select_tab(tab_name)

    def update_tab_positions(self):
        # Mettre à jour les positions Y des onglets
        for index, tab_name in enumerate(self.tab_order):
            tab = self.tabs[tab_name]
            y_position = index * 35  # Les onglets commencent à y=0
           
            tab['container'].place_configure(y=y_position)
            tab['y_position'] = y_position
            
        # Repositionner le bouton 'Nouvel onglet' en bas
        new_tab_y = len(self.tab_order) * 35
        sleep(0.1)
        self.new_tab_button.place_configure(y=new_tab_y)

    def animate_tabs_on_delete(self, start_index):
        steps = 10
        delta = 35 / steps
        for step in range(steps):
            for index in range(start_index, len(self.tab_order)):
                tab_name = self.tab_order[index]
                tab = self.tabs[tab_name]
                new_y = tab['y_position'] - delta
                tab['container'].place_configure(y=new_y)
                tab['y_position'] = new_y
            # Déplacer le bouton 'Nouvel onglet' vers le haut
            new_tab_y = self.new_tab_button.winfo_y() - delta
            self.new_tab_button.place_configure(y=new_tab_y)
            self.tabs_container.update()
            self.after(10)
        self.update_tab_positions()

    def select_tab(self, tab_name):
        self.current_tab = tab_name
        # Masquer tous les contenus des onglets
        for tab in self.tabs.values():
            tab['content'].pack_forget()
        # Afficher le contenu de l'onglet sélectionné
        self.tabs[tab_name]['content'].pack(fill="both", expand=True)

    def delete_tab(self, tab_name):
        index = self.tab_order.index(tab_name)
        tab = self.tabs[tab_name]

        # Supprimer le contenu de l'onglet
        tab['container'].destroy()
        tab['content'].destroy()

        # Supprimer l'onglet des structures de données
        del self.tabs[tab_name]
        self.tab_order.remove(tab_name)

        # Animer les onglets restants pour combler l'espace
        self.animate_tabs_on_delete(start_index=index)

        # Si l'onglet supprimé était le courant, mettre à jour le contenu
        if self.current_tab == tab_name:
            self.current_tab = None
            if self.tab_order:
                self.select_tab(self.tab_order[0])  # Sélectionner le premier onglet
            else:
                for widget in self.content_frame.winfo_children():
                    widget.destroy()

    def open_options(self):
        # Méthode appelée lorsque le bouton 'Options' est cliqué
        messagebox.showinfo("Options", "Les options seront disponibles ici.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
