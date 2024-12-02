
from flask import Blueprint

# Create the blueprint with a unique name and specify the template directory

# Import routes after blueprint creation to avoid circular imports
from . import routes

# # Optional: Register any blueprint-specific error handlers or context processors
# @bp.app_errorhandler(404)
# def handle_404(error):
#     return {'error': 'Resource not found'}, 404

# @bp.app_errorhandler(500)
# def handle_500(error):
#     return {'error': 'Internal server error'}, 500