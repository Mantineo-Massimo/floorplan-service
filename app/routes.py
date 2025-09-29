"""
EN: Defines all web routes for the Floorplan Service.
IT: Definisce tutte le rotte web per il Floorplan Service.
"""
import os
import re
import glob
from pathlib import Path
from flask import Blueprint, render_template, abort, send_from_directory, current_app, jsonify

bp = Blueprint('floorplan', __name__)

@bp.route("/<string:building>/<string:floor_str>/<string:image_name>")
def floor_display(building: str, floor_str: str, image_name: str):
    """
    EN: Dynamically finds and displays a floor plan image, searching recursively.
    IT: Trova e visualizza dinamicamente un'immagine di una planimetria, cercandola ricorsivamente.
    """
    building_key = building.upper()
    
    try:
        floor_number = int(re.sub(r'\D', '', floor_str))
    except (ValueError, TypeError):
        abort(400, "Invalid floor format.")

    building_paths = current_app.config['BUILDING_PATHS']
    allowed_floors = current_app.config['ALLOWED_FLOORS']

    if building_key not in building_paths or floor_number not in allowed_floors:
        abort(404, "Building or floor not found.")

    building_folder = building_paths[building_key]
    ui_folder_abs = os.path.abspath(os.path.join(current_app.root_path, '..', 'ui'))
    assets_root_abs = os.path.join(ui_folder_abs, 'assets')
    base_search_path = os.path.join(assets_root_abs, building_folder, floor_str)

    if not os.path.isdir(base_search_path):
        abort(404, f"Directory for floor '{floor_str}' not found.")

    search_pattern = os.path.join(base_search_path, '**', f'{image_name}.*')
    found_files = glob.glob(search_pattern, recursive=True)

    if not found_files:
        abort(404, f"Image '{image_name}' not found in '{building_key}/{floor_str}'.")

    relative_path = Path(found_files[0]).relative_to(assets_root_abs)
    image_path_for_template = f"/floorplan/assets/{relative_path.as_posix()}"

    return render_template(
        "index.html",
        background_url=image_path_for_template,
        building_name=building_key,
        floor_number=floor_number
    )

@bp.route('/assets/<path:path>')
def serve_assets(path):
    assets_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'ui', 'assets'))
    return send_from_directory(assets_folder, path)

@bp.route('/favicon.ico')
def favicon():
    assets_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'ui', 'assets'))
    return send_from_directory(assets_folder, 'favicon.ico')

@bp.route('/health')
def health_check():
    return jsonify({"status": "ok"})

@bp.errorhandler(404)
def page_not_found(e):
    ui_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'ui'))
    return send_from_directory(ui_folder, '404.html'), 404