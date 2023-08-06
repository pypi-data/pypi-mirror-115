import click

from marcador.bottle import route, run
from marcador.lib import get_session, get_db_path, Bookmark
from jinja2 import Template


@click.command()
@click.option('--hostname', default='127.0.0.1')
@click.option('--port', type=int, default=8080)
def webserver(hostname, port):
    session = get_session(get_db_path())

    @route('/')
    def index():
        bookmarks = session.query(Bookmark).all()
        t = Template("""
<h1> Bookmarks </h1>
 {% for bookmark in bookmarks %}
<li> {{bookmark.creation_date}} - <a href="{{bookmark.url}}">{{bookmark.url}}</a> </li>
 {% endfor %}
        """)
        return t.render(bookmarks=bookmarks)

    run(host=hostname, port=port)
