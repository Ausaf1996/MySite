from app.library import *

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
    app.db = firestore.client()

    app.client = openai.Client(api_key=app.config['OPENAI_API_KEY'])

    with app.app_context():
        # Import parts of our application
        from .routes import main_routes

        # Register Blueprints
        app.register_blueprint(main_routes)

        return app
