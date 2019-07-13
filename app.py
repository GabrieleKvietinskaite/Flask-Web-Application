from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemyplus as wa 

app = Flask(__name__)
app.secret_key = 'many random bytes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)


class Book(db.Model):
    __searchable__ = ['author_name', 'title']

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(50), unique=False, nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    press = db.Column(db.String(50), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    pages = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"Book('{self.author_name}', '{self.title}', '{self.press}', '{self.year}', '{self.pages}', '{self.price}')"

    def __init__(self, author_name, title, press, year, pages, price):
        self.author_name = author_name
        self.title = title
        self.press = press
        self.year = year
        self.pages = pages
        self.price = price


wa.whoosh_index(app, Book)


@app.route("/")
@app.route("/books")
def books():
    data = Book.query.all()
    return render_template('books.html', Book=data)


@app.route('/search')
def search():
    data = Book.query.whoosh_search(request.args.get('query')).all()
    return render_template('books.html', Book=data)


@app.route("/crud")
def crud():
    data = Book.query.all()
    return render_template('crud.html', Book=data)


@app.route("/insert", methods=['POST', 'GET'])
def insert():
    if request.method == "POST":
        author_name = request.form['author_name']
        title = request.form['title']
        press = request.form['press']
        year = request.form['year']
        pages = request.form['pages']
        price = request.form['price']
        book = Book(author_name, title, press, year, pages, price)
        db.session.add(book)
        flash("Data inserted Successfully")
        db.session.commit()
        return redirect(url_for('crud'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    id_data = request.form['id']
    author_name = request.form['author_name']
    title = request.form['title']
    press = request.form['press']
    year = request.form['year']
    pages = request.form['pages']
    price = request.form['price']
    data = Book.query.get(id_data)
    data.author_name = author_name
    data.title = title
    data.press = press
    data.year = year
    data.pages = pages
    data.price = price
    flash("Data Updated Successfully")
    db.session.commit()
    return redirect(url_for('crud'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    data = Book.query.get(id_data)
    db.session.delete(data)
    flash("Record Has Been Deleted Successfully")
    db.session.commit()
    return redirect(url_for('crud'))


@app.route('/about/<string:id_data>', methods=['GET'])
def about(id_data):
    data = Book.query.filter_by(id=id_data)
    return render_template('about.html', Book=data)


if __name__ == "__main__":
    app.run(debug=True)
