import os
from flask import Flask, render_template, abort, url_for

app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",
    template_folder="web"
)

# --- Configurazione Aggiornata ---

# Mappatura dei nomi nell'URL alle cartelle reali
BUILDING_PATHS = {
    "SBA": "SBA",
    "A": "EdificioA"
}
ALLOWED_BUILDINGS = set(BUILDING_PATHS.keys())

# Mappatura completa di tutte le immagini alle loro estensioni
IMAGE_EXTENSIONS = {
    # Immagini in EdificioA
    "3_docenti": ".jpg",
    "A_docenti": ".jpg",
    "B_docenti": ".jpg",
    "blocco3": ".jpg",
    "bloccoA": ".jpg",
    "bloccoB": ".jpg",
    "bloccoC": ".jpg",
    "bloccoD": ".jpg",
    "C_docenti": ".jpg",
    "D_docenti": ".jpg",
    "grassano": ".jpg",
    
    # Immagini in SBA
    "dx-up": ".png",
    "dx-down": ".png",
    "sx-up": ".png",
    "sx-down": ".png",
    "sx-ip": ".png"
}

ALLOWED_FILENAMES = set(IMAGE_EXTENSIONS.keys())
# Ho aggiunto il piano 3
ALLOWED_FLOORS = {0, 1, 2, 3} 

@app.route("/<building>/floor<int:floor>/<image_name>")
def floor_display(building, floor, image_name):
    """
    Mostra un'immagine della planimetria partendo da un URL senza estensione del file.
    """
    building_upper = building.upper()

    # Controllo di validità
    if (building_upper not in ALLOWED_BUILDINGS or
            floor not in ALLOWED_FLOORS or
            image_name not in ALLOWED_FILENAMES):
        abort(404)

    # Ricostruisce il nome del file con l'estensione corretta
    extension = IMAGE_EXTENSIONS[image_name]
    full_filename = f"{image_name}{extension}"

    # Usa la mappatura per trovare la cartella corretta
    building_folder = BUILDING_PATHS[building_upper]
    file_path_for_url = f"assets/{building_folder}/floor{floor}/{full_filename}"
    
    # Percorso completo che verrà cercato sul disco
    full_path_on_disk = os.path.join(app.static_folder, file_path_for_url)
    
    # Stampa di debug per verificare il percorso esatto
    print(f"DEBUG: Checking for file at path: '{full_path_on_disk}'")

    if not os.path.exists(full_path_on_disk):
        print(f"DEBUG: File NOT FOUND at '{full_path_on_disk}'. Aborting with 404.")
        abort(404)

    bg_url = url_for('static', filename=file_path_for_url)
    
    return render_template("index.html",
                           bg_url=bg_url,
                           building=building_upper,
                           floor=floor)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
