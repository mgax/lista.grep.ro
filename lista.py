import py.path
import yaml
import flask
import flask_frozen

app = flask.Flask(__name__)
freezer = flask_frozen.Freezer(app)


def load_articles(articles_dir_path):
    articles = []
    for article_path in articles_dir_path.listdir():
        article_id = article_path.basename.rsplit('.', 1)[0]
        with article_path.open('rb') as f:
            header = ""
            lines = (l.decode('utf-8') for l in f)
            for line in lines:
                if line.strip() == '---':
                    break
                header += line
            content = ''.join(lines)
            articles.append(dict(yaml.load(header),
                                 id=article_id,
                                 content=content))
    return articles


articles = load_articles(py.path.local(__file__).dirpath().join('articles'))


@app.route('/')
def homepage():
    return flask.render_template('index.html', articles=articles)


if __name__ == '__main__':
    freezer.freeze()
    freezer.serve()
