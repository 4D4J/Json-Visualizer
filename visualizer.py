import json
import customtkinter as ctk
from tkinter import filedialog
from tkinter import Tk

# Fonction pour charger les données d'un fichier JSON sélectionné par l'utilisateur
def load_data():
    # Ouvrir une fenêtre de sélection de fichiers dans l'interface
    file_path = filedialog.askopenfilename(
        title="Sélectionner un fichier JSON", 
        filetypes=[("Fichiers JSON", "*.json")]
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                return json.load(f)
    else:
        return None

# Fonction pour créer l'interface graphique
def create_interface():
    # Fonction pour filtrer la liste
    def filter_list():
        query = search_entry.get().lower()
        for widget in frame.winfo_children():
            widget.destroy()

        filtered_data = {key: value for key, value in data.items() if query in key.lower() or any(query in str(val).lower() for val in value.values())}
        display_data(filtered_data)
        update_item_count(len(filtered_data))

    # Fonction pour afficher les données JSON
    def display_data(json_data):
        for key, values in json_data.items():
            key_label = ctk.CTkLabel(frame, text=key, font=("Arial", 16, "bold"))
            key_label.pack(anchor="w", padx=10, pady=5)

            if isinstance(values, dict):
                for sub_key, sub_value in values.items():
                    sub_label = ctk.CTkLabel(frame, text=f"{sub_key}: {sub_value}", font=("Arial", 14))
                    sub_label.pack(anchor="w", padx=30)
            else:
                value_label = ctk.CTkLabel(frame, text=str(values), font=("Arial", 14))
                value_label.pack(anchor="w", padx=30)

    # Fonction pour mettre à jour le nombre d'éléments affichés
    def update_item_count(count):
        item_count_label.configure(text=f"Nombre d'éléments : {count}")

    # Fonction pour charger et afficher un fichier JSON sélectionné
    def load_and_display_json():
        global data
        data = load_data()
        if data:
            for widget in frame.winfo_children():
                widget.destroy()
            display_data(data)
            update_item_count(len(data))

    # Configuration principale de l'interface
    root = ctk.CTk()
    root.title("Visualiseur JSON")
    root.geometry("600x500")
    root.configure(fg_color="#2b2b2b")

    # Rendre la fenêtre responsive
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(4, weight=1)

    # Titre de l'application
    title_label = ctk.CTkLabel(root, text="Visualiseur JSON", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, pady=10)

    # Bouton pour choisir le fichier JSON
    load_button = ctk.CTkButton(root, text="Choisir un fichier JSON", command=load_and_display_json)
    load_button.grid(row=1, column=0, padx=20, pady=10)

    # Barre de recherche
    search_entry = ctk.CTkEntry(root, placeholder_text="Rechercher...")
    search_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
    search_entry.bind("<KeyRelease>", lambda event: filter_list())  # Détecte la saisie pour filtrer

    # Affichage du nombre d'éléments
    item_count_label = ctk.CTkLabel(root, text="Nombre d'éléments : 0", font=("Arial", 16))
    item_count_label.grid(row=3, column=0, pady=10)

    # Cadre pour afficher les données (scrollable)
    frame = ctk.CTkScrollableFrame(root, width=550, height=300)
    frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

    root.mainloop()

# Initialiser et lancer l'interface
create_interface()
