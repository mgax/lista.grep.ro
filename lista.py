import py.path
import flask
import flask_frozen

app = flask.Flask(__name__)
freezer = flask_frozen.Freezer(app)


def load_articles(articles_dir_path):
    articles = {}
    for article_path in articles_dir_path.listdir():
        article_id = article_path.basename.rsplit('.', 1)[0]
        with article_path.open('rb') as f:
            articles[article_id] = f.read()
    return articles


articles = load_articles(py.path.local(__file__).dirpath().join('articles'))


@app.route('/')
def homepage():
    return 'hello world'


if __name__ == '__main__':
    freezer.freeze()
    freezer.serve()
