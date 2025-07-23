"""
WSGI entrypoint for the Floorplan Display Service.
Serves a static UI for displaying building floor plans by rendering a template
with the correct background image based on URL parameters.
"""
import os
from flask import Flask, render_template, abort

app = Flask(
    __name__,
    static_folder="ui",
    static_url_path="",
    template_folder="ui"
)

# --- Configuration: Define allowed paths and image types ---
BUILDING_PATHS = { "A": "building_a", "B": "building_b", "SBA": "building_sba" }
ALLOWED_FLOORS = {-1, 0, 1, 2, 3}
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

@app.route("/<string:building>/floor<int:floor>/<string:image_name>")
def floor_display(building: str, floor: int, image_name: str):
    """
    Renderizza il visualizzatore di planimetrie con l'immagine di sfondo corretta.
    Esempio URL: /A/floor1/blockA
    """
    building_key = building.upper()

    if (building_key not in BUILDING_PATHS or
            floor not in ALLOWED_FLOORS or
            image_name not in IMAGE_EXTENSIONS):
        abort(404, description="Edificio, piano o nome immagine non validi.")

    building_folder = BUILDING_PATHS[building_key]
    image_extension = IMAGE_EXTENSIONS[image_name]
    full_filename = f"{image_name}{image_extension}"
    
    image_path_for_template = f"/assets/{building_folder}/floor{floor}/{full_filename}"
    
    full_disk_path = os.path.join(app.static_folder, 'assets', building_folder, f"floor{floor}", full_filename)
    
    if not os.path.exists(full_disk_path):
        abort(404, description=f"File immagine non trovato: {full_disk_path}")

    return render_template(
        "index.html",
        background_url=image_path_for_template,
        building_name=building_key,
        floor_number=floor
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)