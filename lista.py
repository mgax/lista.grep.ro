import flask
import flask_frozen

app = flask.Flask(__name__)
freezer = flask_frozen.Freezer(app)


@app.route('/')
def homepage():
    return 'hello world'


if __name__ == '__main__':
    freezer.freeze()
    freezer.serve()
