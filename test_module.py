import customtkinter as ctk
from tkinter import StringVar

# Créer l'application
root = ctk.CTk()

# Créer une StringVar pour gérer la valeur par défaut
default_value = StringVar(value="Valeur par défaut")

# Créer l'entrée avec la variable liée
entry = ctk.CTkEntry(root, textvariable=default_value)
entry.pack(pady=10)

root.mainloop()
