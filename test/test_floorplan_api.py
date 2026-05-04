"""
EN: Automated tests for the Floorplan Service API endpoints.
IT: Test automatici per gli endpoint API del Floorplan Service.
"""
import pytest
import requests

# EN: The base URL points to the Nginx proxy.
# IT: L'URL di base punta al proxy Nginx.
BASE_URL = "http://127.0.0.1:80"

def test_health_check_endpoint():
    """
    EN: Tests the /health endpoint for a 200 OK response.
    IT: Testa l'endpoint /health per una risposta 200 OK.
    """
    response = requests.get(f"{BASE_URL}/floorplan/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_floor_display_success():
    """
    EN: Tests a successful request to a valid floor plan URL using the folder name.
    IT: Testa una richiesta valida usando il nome della cartella.
    """
    response = requests.get(f"{BASE_URL}/floorplan/a/floor_0/A-S-1")
    assert response.status_code == 200
    assert "text/html" in response.headers['Content-Type']

def test_floor_display_numeric_success():
    """
    EN: Tests a successful request using just the floor number (flexible matching).
    IT: Testa una richiesta valida usando solo il numero del piano (matching flessibile).
    """
    # EN: This should match 'floor_0' even if we only send '0'.
    # IT: Dovrebbe trovare 'floor_0' anche se inviamo solo '0'.
    response = requests.get(f"{BASE_URL}/floorplan/a/0/A-S-1")
    assert response.status_code == 200
    assert "text/html" in response.headers['Content-Type']

def test_floor_display_not_found_image():
    """
    EN: Tests a request for an image that does not exist.
    Expects a 404 Not Found response.
    IT: Testa una richiesta per un'immagine che non esiste.
    Si aspetta una risposta 404 Not Found.
    """
    response = requests.get(f"{BASE_URL}/floorplan/A/floor0/IMMAGINE_INESISTENTE")
    assert response.status_code == 404

def test_floor_display_not_found_building():
    """
    EN: Tests a request for a building that is not configured.
    Expects a 404 Not Found response.
    IT: Testa una richiesta per un edificio non configurato.
    Si aspetta una risposta 404 Not Found.
    """
    response = requests.get(f"{BASE_URL}/floorplan/Z/floor0/A-S-1")
    assert response.status_code == 404