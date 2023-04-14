from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class school(db.Model):
    iD = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Physics = db.Column(db.String)
    Chemistry = db.Column(db.String)
    Maths = db.Column(db.String)

@app.route('/', methods = ['POST', 'GET'])
def Student():
    if request.method == 'POST':
        name_content = request.form['Name']
        physic_content = request.form['Physics']
        chemistry_content = request.form['Chemistry']
        math_content = request.form['Maths']
        new_content = school(Name=name_content, Physics=physic_content, Chemistry=chemistry_content,Maths=math_content)

        try:
            db.session.add(new_content)
            db.seesion.commit()
            return redirect('/result')

        except:
            return 'There was an error.'

    else:
        results = school.query.all()
        return render_template("index.html", results=results)


if __name__ == '__main__':
    app.run(debug=True)