"""#init file is used as an application factory, there file is not run unless called

import os #Importing OS allows to run CML inside python script
from flask import Flask

def create_app(test_config=None):
    # create and configure app
    # instance_relative= True tells app that configuration files are relative to instance folder
    app = Flask(__name__, instance_relative_config=True)
    # sets some default configuration that app will use
    app.config.from_mapping(
        # used to keep data safe, set to dev to provide convenient value during development but should be changed before deploying
        SECRET_KEY='dev',
        # Database is where SQLite db will be saved, its under app.instance_path
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) #If file doesn't exist it will 'fail' silently
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedir(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return render_template('base.html')

    #import db and call function to add command to initialize database
    from . import db
    db.init_app(app)

    from flaskr import auth
    app.register_blueprint(auth.bp)

    # unlike auth bp, blog bp does not have url prefix
    # so the index view will be at /, in otherwords if logged in always auto route to index
    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_for('/', endpoint='index')

    return app"""