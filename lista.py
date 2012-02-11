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


events = load_events(py.path.local(__file__).dirpath().join('events'))


@app.route('/')
def homepage():
    return flask.render_template('index.html', events=events)


def main():
    freezer.freeze()
    freezer.serve()


if __name__ == '__main__':
    import os.path
    from werkzeug.serving import run_with_reloader
    app.debug = True
    extra_files = [os.path.join(app.template_folder, name) for name in
                   [''] + os.listdir(app.template_folder)]
    run_with_reloader(main, extra_files)
