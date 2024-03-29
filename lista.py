#!/usr/bin/env python

import operator
from datetime import datetime
import urlparse
from path import path
import yaml
import flask
from flask.ext.frozen import Freezer
from flask.ext.script import Manager
from werkzeug.contrib.atom import AtomFeed


app = flask.Flask(__name__)
freezer = Freezer(app)
manager = Manager(app)
app.config.from_pyfile('settings.py', silent=True)


def load_events(events_dir_path):
    events = []
    for event_path in events_dir_path.listdir():
        event_id = event_path.name.rsplit('.', 1)[0]
        with event_path.open('rb') as f:
            event_data = yaml.load(f)
            event_data['id'] = event_id
            event_data.setdefault('change-date', event_data['post-date'])
            events.append(event_data)
    events.sort(key=operator.itemgetter('date'), reverse=True)
    return events


events_folder = path(__file__).parent / 'events'
events = load_events(events_folder)


@app.before_request
def load_events_before_request():
    global events
    events = load_events(events_folder)


@app.context_processor
def inject_template_globals():
    return {
        'site_title': "Lista hackerului social",
    }


@app.route('/')
def homepage():
    return flask.render_template('index.html', events=events)


@app.route('/communities.html')
def communities():
    return flask.render_template('communities.html')


@app.route('/recent.atom')
def recent_atom():
    """ Deprecated feedburner feed """
    site_url = 'http://lista.grep.ro/'
    feed = AtomFeed("Lista hackerului social (feed vechi)",
                    feed_url=urlparse.urljoin(site_url, flask.request.path),
                    url=site_url)

    event_date = datetime(2013, 3, 14)
    feed.add(u"Feed nou",
             flask.render_template('old_feed.html'),
             id='{site_url}entry/2013-03-14-feed-nou'.format(**locals()),
             url=site_url,
             updated=event_date,
             published=event_date,
             author="Alex Morega")
    return feed.get_response()


@app.route('/feed.atom')
def feed_atom():
    site_url = 'http://lista.grep.ro/'
    tmpl = flask.current_app.jinja_env.get_template('feed_item.html')
    feed = AtomFeed("Lista hackerului social",
                    feed_url=urlparse.urljoin(site_url, flask.request.path),
                    url=site_url)

    ordered_events = sorted(events, key=operator.itemgetter('change-date'))
    for event in reversed(ordered_events[-20:]):
        if event['post-date'] < datetime(2012, 11, 23):
            item_id = event['url']
        else:
            item_id = '{site_url}entry/{event[id]}'.format(**locals())
        feed.add(u"%s (%s)" % (event['title'],
                               event['date'].strftime('%d %b')),
                 unicode(tmpl.render(event=event)),
                 id=item_id,
                 url=event['url'],
                 updated=event['change-date'],
                 published=event['post-date'],
                 author="Alex Morega")
    return feed.get_response()


@manager.command
def build():
    freezer.freeze()


if __name__ == '__main__':
    manager.run()
