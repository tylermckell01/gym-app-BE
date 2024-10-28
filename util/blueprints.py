import routes


def register_blueprints(app):
    app.register_blueprint(routes.workout)
    app.register_blueprint(routes.exercises)
    app.register_blueprint(routes.gyms)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.auth)
