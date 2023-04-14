#An object of Flask class is our WSGI application
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask constructor takes the name of
# current module (__name__) as argument
# set template_folder= name of whatever folder you are keeping templates
app = Flask(__name__, template_folder= 'template')

# Tell app where database is located (qlite)
# /// = relative path - don't have to specify exact location of test.db file
# //// = Absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize database and pass in app
db = SQLAlchemy(app)

# Create Todo class to house all data in set columns
class Todo(db.Model):
    # Id data column to track each entry to integer
    # Primary key = first column
    id = db.Column(db.Integer, primary_key=True)

    # Column for text input from user w/ max 200 words
    # Nullable = False means cant be left blank
    content = db.Column(db.String(200), nullable = False)

    # Column to record time of input set to current time at input
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Everytime new element is made repr function return task and self.id of task created
    def __repr__(self):
        return '<Task %r>' % self.id


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# & associated function/s to run (binds URL to function).
# methods POST & GET are passed in to allow sending and retrieving data from db
@app.route('/', methods=['POST', 'GET'])
def index():
    # If user clicks on HTML form created in which the method is POST
    # Save HTML 'content' as task_content
    # & and save task_content as db content
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # Try adding new_task to db
        # Commit new_task to db
        # Return to the main page
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        # Otherwise if the try doesnt work
        # Return error message
        except:
            return 'There was an issue adding you task'

    # If the user hasn't clicked on the Add Task (POST) button
    # Request all tasks in db in order created
    # & render them on main html page
    # tasks = tasks relates to jinja2 syntax in html page
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

# Delete route with delete link and id passed in
# User clicks link app routes to delete function
@app.route('/delete/<int:id>')
def delete(id):
    # Attempt to get task by id and if doesn't exist return 404
    task_to_delete = Todo.query.get_or_404(id)

    # Try to delete task_to_delete based on task id
    # Commit delete
    # Return to main page
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    # Return except if cant be deleted
    except:
        return 'There was a problem deleting that task.'

# Update route with update link and id passed in
# User clicks update app routes to update page
# If user clicks update button method == post
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    # If user clicks button form input is saved as task content
    if request.method == 'POST':
        task.content = request.form['content']

        # Try commit new input in existing content saved in db (re-writes content)
        # return to main page
        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was a problem updating this task.'
    # if not press button render update html page with task == db task
    else:
        return render_template('update.html', task = task)

# Main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug = True)
    # Any errors will pop up on webpage w/