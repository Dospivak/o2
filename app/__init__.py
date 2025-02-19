from flask import Flask
import os

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Set the secret key for session
    app.secret_key = 'your-secret-key-here'
    
    # Import and register blueprints/routes
    from app.routes import main_routes
    app.register_blueprint(main_routes.bp)
    
    return app 