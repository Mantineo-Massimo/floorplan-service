import os
import re
import glob
from pathlib import Path
from flask import Flask, render_template, abort, send_from_directory

app = Flask(
    __name__,
    static_folder="ui",
    template_folder="ui"
)

# --- Configurazione ---
# MODIFICATO: Aggiunto l'edificio B
BUILDING_PATHS = { "A": "building_A", "SBA": "building_SBA", "B": "building_B" }
ALLOWED_FLOORS = {-1, 0, 1, 2, 3}

# --- Rotta Principale per le Planimetrie ---
@app.route("/<string:building>/<string:floor_str>/<string:image_name>")
def floor_display(building: str, floor_str: str, image_name: str):
    """
    Trova e visualizza dinamicamente un'immagine di una planimetria,
    cercandola ricorsivamente nella cartella del piano specificato.
    """
    building_key = building.upper()

    try:
        # Estrae il numero dal piano, gestendo anche stringhe come 'piano0'
        floor_number = int(re.sub(r'\D', '', floor_str) or 0)
    except (ValueError, TypeError):
        abort(400, "Formato del piano non valido.")

    # I piani per l'edificio B (0, 1, 2, 3) sono già inclusi in ALLOWED_FLOORS
    if building_key not in BUILDING_PATHS or floor_number not in ALLOWED_FLOORS:
        abort(404, "Edificio o piano non trovato.")

    building_folder = BUILDING_PATHS[building_key]
    
    base_search_path = os.path.join(app.static_folder, 'assets', building_folder, floor_str)

    if not os.path.isdir(base_search_path):
        abort(404, f"La cartella per il piano '{floor_str}' non esiste.")

    search_pattern = os.path.join(base_search_path, '**', f'{image_name}.*')
    found_files = glob.glob(search_pattern, recursive=True)

    if not found_files:
        abort(404, f"Immagine '{image_name}' non trovata in '{building_key}/{floor_str}'.")

    full_disk_path = found_files[0]
    
    assets_root = Path(app.static_folder) / 'assets'
    relative_path = Path(full_disk_path).relative_to(assets_root)
    
    # Questo assicura che il browser invii la richiesta a Nginx,
    # che la inoltrerà correttamente a questa applicazione Flask.
    image_path_for_template = f"/floorplan/assets/{relative_path.as_posix()}"

    return render_template(
        "index.html",
        background_url=image_path_for_template,
        building_name=building_key,
        floor_number=floor_number
    )

# --- Rotte per i File Statici ---
# Queste rotte sono necessarie affinché il template HTML possa caricare
# le immagini e altri file statici.

@app.route('/static/<path:path>')
def serve_static_files(path):
    """Serve i file statici come CSS e JavaScript."""
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

@app.route('/favicon.ico')
def favicon():
    """Serve il favicon dalla cartella ui/assets/"""
    return send_from_directory(os.path.join(app.static_folder, 'assets'), 'favicon.ico')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)