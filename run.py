from api import app
from api import routes
from flask import render_template

# Register API Blueprint
app.register_blueprint(routes.mod)

# Route to Index Page
@app.route('/')
def index():
    """
    Route to Index Page
    :return: Hello World on Index Page
    """
    return render_template('documentation.html')


if __name__ == '__main__':
    """
    Starts Flask Server Once File is run
    """
    app.run(debug=True)
