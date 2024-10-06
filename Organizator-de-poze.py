import os
import shutil
import time
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox
from tkinter.ttk import Progressbar
from tqdm import tqdm

# Funcție pentru mutarea fișierului în folderul corespunzător pe baza extensiei
def move_file(file_path, filename, target_directory, extension):
    try:
        # Creează folderul pentru extensia respectivă
        extension_folder = os.path.join(target_directory, extension[1:])  # Înlătură punctul din extensie
        
        if not os.path.exists(extension_folder):
            os.makedirs(extension_folder)
        
        # Mută fișierul în folderul corespunzător
        shutil.move(file_path, os.path.join(extension_folder, filename))
        return True
    except Exception as e:
        print(f"Eroare la mutarea fișierului {filename}: {e}")
        return False

# Funcție principală de organizare
def organize_files(source_directory, target_directory, extensions):
    files = [f for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f))]
    total_files = len(files)
    
    moved_files = 0
    errors = 0

    # Actualizăm bara de progres
    for i, filename in enumerate(tqdm(files)):
        file_path = os.path.join(source_directory, filename)
        extension = os.path.splitext(filename)[1].lower()

        # Mută doar fișierele care au extensia dorită
        if extension in extensions:
            success = move_file(file_path, filename, target_directory, extension)
            if success:
                moved_files += 1
            else:
                errors += 1

        # Actualizăm bara de progres
        progress['value'] = (i + 1) / total_files * 100
        root.update_idletasks()

    # Afișăm raportul
    messagebox.showinfo("Rezultate", f"Fișiere mutate: {moved_files}\nErori: {errors}")

# Funcție pentru a selecta un director
def select_directory(var):
    folder_selected = filedialog.askdirectory()
    var.set(folder_selected)

# Inițializare fereastră Tkinter
root = Tk()
root.title("Organizator de fișiere")

# Variabile pentru directorul sursă și țintă
source_var = StringVar()
target_var = StringVar()
extensions_var = StringVar(value=".jpg .png .cr2")

# Etichete și intrări pentru selectarea directorului sursă și țintă
Label(root, text="Director sursă:").grid(row=0, column=0)
Entry(root, textvariable=source_var).grid(row=0, column=1)
Button(root, text="Selectează", command=lambda: select_directory(source_var)).grid(row=0, column=2)

Label(root, text="Director țintă:").grid(row=1, column=0)
Entry(root, textvariable=target_var).grid(row=1, column=1)
Button(root, text="Selectează", command=lambda: select_directory(target_var)).grid(row=1, column=2)

# Intrare pentru extensii de fișiere
Label(root, text="Extensii de fișiere (separate prin spațiu):").grid(row=2, column=0)
Entry(root, textvariable=extensions_var).grid(row=2, column=1)

# Bara de progres
progress = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.grid(row=3, column=1)

# Buton pentru rularea funcției de organizare
Button(root, text="Organizează fișierele", command=lambda: organize_files(source_var.get(), target_var.get(), extensions_var.get().split())).grid(row=4, column=1)

# Rulăm aplicația Tkinter
root.mainloop()