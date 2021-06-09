from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    page = db.Column(db.String(100))

    def __init__(self, name, title, author,isbn,publisher,page):
        self.name = name
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.page = page

@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", Users=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        publisher = request.form['publisher']
        page = request.form['page']

        my_data = Data(name, title, author,isbn,publisher,page)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.isbn = request.form['isbn']
        my_data.publisher = request.form['publisher']
        my_data.page = request.form['page']


        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)