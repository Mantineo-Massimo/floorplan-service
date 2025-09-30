"""
EN: Application factory for the Floorplan Service.
IT: "Application factory" per il Floorplan Service.
"""
import redis
from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman
from . import config

def create_app():
    """
    EN: Creates and configures the Flask application instance.
    IT: Crea e configura l'istanza dell'applicazione Flask.
    """
    app = Flask(
        __name__,
        static_folder='../ui/static',
        template_folder='../ui'
    )
    
    app.config.from_object(config)
    
    # EN: Create a Redis connection pool and attach it to the app instance.
    # IT: Crea un pool di connessioni Redis e lo collega all'istanza dell'app.
    app.redis = redis.from_url(app.config['REDIS_URL'])

    # EN: Define a Content Security Policy (CSP) that allows inline styles for the background.
    # IT: Definisce una Content Security Policy (CSP) che permette gli stili inline per lo sfondo.
    csp = {
        'default-src': "'self'",
        'style-src': ["'self'", "'unsafe-inline'"]
    }
    
    CORS(app)
    Talisman(app, force_https=False, content_security_policy=csp)

    from .routes import bp
    app.register_blueprint(bp)
    
    return app