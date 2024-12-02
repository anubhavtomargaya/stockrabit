# wsgi.py

import os
# from dotenv import load_dotenv
from astrocub import create_app
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file if it exists
# load_dotenv()

# Determine the environment (development, production, etc.)
# ENV = os.getenv('FLASK_ENV', 'production')

# Create the Flask application instance
app = create_app()

# # Configure logging
# if not app.debug:
#     # Ensure the logs directory exists
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
    
#     # Create a file handler that logs even debug messages
#     file_handler = RotatingFileHandler(
#         'logs/astrocub.log',
#         maxBytes=10240000,  # 10MB
#         backupCount=10      # Keep 10 backup copies
#     )
    
#     # Set the logging format
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s '
#         '[in %(pathname)s:%(lineno)d]'
#     ))
    
#     # Set the logging level
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
    
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Astrocub startup')

# # This block only runs if we execute this file directly
# if __name__ == '__main__':
#     # For development server only
#     app.run(
#         host=os.getenv('FLASK_HOST', '0.0.0.0'),
#         port=int(os.getenv('FLASK_PORT', 5000)),
#         debug=ENV == 'development'
#     )


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=5000,debug=True)