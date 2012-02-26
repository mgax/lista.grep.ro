import operator
import urlparse
import py.path
import yaml
import flask
import flask_frozen
import flaskext.script
from werkzeug.contrib.atom import AtomFeed


app = flask.Flask(__name__)
freezer = flask_frozen.Freezer(app)
manager = flaskext.script.Manager(app)
app.config.from_pyfile('settings.py', silent=True)


def load_events(events_dir_path):
    events = []
    for event_path in events_dir_path.listdir():
        event_id = event_path.basename.rsplit('.', 1)[0]
        with event_path.open('rb') as f:
            event_data = yaml.load(f)
            event_data['id'] = event_id
            event_data.setdefault('change-date', event_data['post-date'])
            events.append(event_data)
    events.sort(key=operator.itemgetter('date'), reverse=True)
    return events


events_folder = py.path.local(__file__).dirpath().join('events')
events = load_events(events_folder)


@app.route('/')
def homepage():
    return flask.render_template('index.html', events=events)


@app.route('/recent.atom')
def recent_atom():
    site_url = 'http://lista.grep.ro/'
    tmpl = flask.current_app.jinja_env.get_template('feed_item.html')
    feed = AtomFeed("Lista hackerului social",
                    feed_url=urlparse.urljoin(site_url, flask.request.path),
                    url=site_url)

    ordered_events = sorted(events, key=operator.itemgetter('change-date'))
    for event in reversed(ordered_events[-20:]):
        feed.add(u"%s (%s)" % (event['title'],
                               event['date'].strftime('%d %b')),
                 unicode(tmpl.render(event=event)),
                 url=event['url'],
                 updated=event['change-date'],
                 published=event['post-date'],
                 author="Alex Morega")
    return feed.get_response()


@manager.command
def build():
    freezer.freeze()


@manager.command
def devel():
    from werkzeug.serving import run_with_reloader
    app.debug = True
    extra_files = [str(p) for p in
                   list(py.path.local(app.template_folder).visit()) +
                   list(py.path.local(app.static_folder).visit()) +
                   list(events_folder.visit())]

    def iterate():
        freezer.freeze()
        freezer.serve()

    run_with_reloader(iterate, extra_files)


if __name__ == '__main__':
    manager.run()
