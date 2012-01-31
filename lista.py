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
            header = ""
            lines = (l.decode('utf-8') for l in f)
            for line in lines:
                if line.strip() == '---':
                    break
                header += line
            content = ''.join(lines)
            events.append(dict(yaml.load(header),
                                 id=event_id,
                                 content=content))
    return events


events = load_events(py.path.local(__file__).dirpath().join('events'))


@app.route('/')
def homepage():
    return flask.render_template('index.html', events=events)


if __name__ == '__main__':
    freezer.freeze()
    freezer.serve()
