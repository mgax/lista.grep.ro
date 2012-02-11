import py.path
import yaml
import flask
import flask_frozen

app = flask.Flask(__name__)
freezer = flask_frozen.Freezer(app)


def load_events(events_dir_path):
    events = []
    for event_path in events_dir_path.listdir():
        event_id = event_path.basename.rsplit('.', 1)[0]
        with event_path.open('rb') as f:
            event_data = yaml.load(f)
            event_data['id'] = event_id
            events.append(event_data)
    return events


events_folder = py.path.local(__file__).dirpath().join('events')
events = load_events(events_folder)


@app.route('/')
def homepage():
    return flask.render_template('index.html', events=events)


def main():
    freezer.freeze()
    freezer.serve()


def devel():
    from werkzeug.serving import run_with_reloader
    app.debug = True
    extra_files = [str(p) for p in
                   list(py.path.local(app.template_folder).visit()) +
                   list(py.path.local(app.static_folder).visit()) +
                   list(events_folder.visit())]
    run_with_reloader(main, extra_files)


if __name__ == '__main__':
    devel()
