"""import sqlite3
import click
from flask import current_app, g


def get_db():
    #g is special object unique for each request,
    # stores data that might be accessed by multiple functions during the request
    if 'db' not in g:
        #sqlite3.conntect establishes a connection to the file pointed at by database config key
        g.db = sqlite3.connect(
            # current_app points to flask app handling request
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #sqlite3.Row tells connection to return rows that behave like dicts. allows accessing columns by name
        g.db.row_factory = sqlite3.Row

    return g.db


# checks if connection was creating by checking if g.db was set,
# If exists, it is closed
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # returns database connection - execute commands read from file
    db = get_db()

    # opens file relative to flaskr package,
    # as may not know where location is when deploying app
    with current_app.open_resource('schema.sql') as f:
        #read and run file
        db.executescript(f.read().decode('utf8'))

# defines command line command called init-db
# command calls init_db function and shows message to user
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# close_db and init_db_command functions need be registed w/ app instance
# Otherwise won't be used by app
# Since we are using factory function that instance isn't available when writing the functions
# Instead, write function takes app and does registration

def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # adds new command that can be called with flask command
    app.cli.add_command(init_db_command)

# call flask -- app flask init-db in command line to initialize db"""
