# astrocub/__init__.py
from flask import Flask
from flask_cors import CORS
# from .core.extensions import init_extensions
# from .core.database import init_db
from .blueprints.genetl.routes import bp
def create_app(config=None):
    """Application factory function"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    # if config is None:
    #     app.config.from_object('astrocub.config.DevelopmentConfig')
    # else:
    #     app.config.from_object(config)
    
    # Load instance config if it exists
    # app.config.from_pyfile('config.py', silent=True)
    
    # Initialize extensions
    # init_extensions(app)
    # init_db(app)
    CORS(app)
    
    # Register blueprints
    # from .blueprints.genetl import bp as genetl_bp
    app.register_blueprint(bp, url_prefix='/genetl')
    
    return app