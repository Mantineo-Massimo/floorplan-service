import os
import re
from flask import Flask, render_template, abort, send_from_directory

app = Flask(
    __name__,
    static_folder="ui",
    template_folder="ui"
)

# --- Configurazione ---
BUILDING_PATHS = { "A": "building_a", "B": "building_b", "SBA": "building_sba" }
ALLOWED_FLOORS = {-1, 0, 1, 2, 3}
IMAGE_EXTENSIONS = {
    "3_docenti": ".jpg", "A_docenti": ".jpg", "B_docenti": ".jpg", "blocco3": ".jpg",
    "bloccoA": ".jpg", "bloccoB": ".jpg", "bloccoC": ".jpg", "bloccoD": ".jpg",
    "C_docenti": ".jpg", "D_docenti": ".jpg", "grassano": ".jpg", "dx-up": ".png",
    "dx-down": ".png", "sx-up": ".png", "sx-down": ".png", "sx-ip": ".png"
}

# --- Rotta Principale per le Planimetrie ---
@app.route("/<string:building>/<string:floor_str>/<string:image_name>")
def floor_display(building: str, floor_str: str, image_name: str):
    # ... (codice non modificato)
    building_key = building.upper()
    try:
        floor_number = int(re.sub(r'\D', '', floor_str) or 0)
    except (ValueError, TypeError):
        abort(400)
    if (building_key not in BUILDING_PATHS or
            floor_number not in ALLOWED_FLOORS or
            image_name not in IMAGE_EXTENSIONS):
        abort(404)
    building_folder = BUILDING_PATHS[building_key]
    image_extension = IMAGE_EXTENSIONS[image_name]
    full_filename = f"{image_name}{image_extension}"
    image_path_for_template = f"/floorplan/assets/{building_folder}/{floor_str}/{full_filename}"
    full_disk_path = os.path.join(app.static_folder, 'assets', building_folder, floor_str, full_filename)
    if not os.path.exists(full_disk_path):
        abort(404)
    return render_template(
        "index.html",
        background_url=image_path_for_template,
        building_name=building_key,
        floor_number=floor_number
    )

# --- Rotte per i File Statici ---
@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory(os.path.join(app.static_folder, 'static'), path)

@app.route('/assets/<path:path>')
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), path)

# MODIFICA: La funzione favicon ora cerca il file dentro la cartella 'assets'
@app.route('/favicon.ico')
def favicon():
    """Serve il favicon dalla cartella ui/assets/"""
    return send_from_directory(os.path.join(app.static_folder, 'assets'), 'favicon.ico')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)