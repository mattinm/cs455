def register_blueprints(app):
    """Registers our blueprints with the given Flask app."""
    
    from .patient import patient
    from .staff import staff
    
    app.register_blueprint(patient, url_prefix='/patient')
    app.register_blueprint(staff, url_prefix='/staff')