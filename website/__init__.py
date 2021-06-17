from flask import Flask


def create_app():
    app = Flask(__name__)  # current name file
    app.config['SECRET_KEY'] = 'wakwoaowakoa'  # encrypt our app

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
