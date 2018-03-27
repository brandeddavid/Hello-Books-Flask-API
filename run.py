from flask import Flask
from api import routes

app = Flask(__name__)

app.register_blueprint(routes.mod)


@app.route('/')
def index():
    """
    Route to Index Page
    :return: Hello World on Index Page
    """
    return 'Hello World'


if __name__ == '__main__':
    """
        Starts Flask Server Once File is run
    """
    app.run(debug=True)
