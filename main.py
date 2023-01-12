from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsadadqwdqsqw'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-project.db"
Bootstrap4(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)


new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)


class EditForm(FlaskForm):
    rating = StringField(label="New rating", validators=[DataRequired()])
    review = StringField(label="New review", validators=[DataRequired()])
    submit = SubmitField()



app.app_context().push()
db.create_all()

@app.route("/")
def home():
    new_movie = Movie(
        title="Phone Booth",
        year=2002,
        description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        rating=7.3,
        ranking=10,
        review="My favourite character was the caller.",
        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    )
    all_films = db.session.query(Movie).all()
    return render_template("index.html", all_films=all_films)


@app.route("/edit/<int:film_id>", methods=["POST", "GET"])
def edit(film_id):
    film_to_edit = Movie.query.get(film_id)
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        film_to_edit.rating = float(request.form["rating"])
        film_to_edit.review = request.form["review"]
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", film=film_to_edit, form=edit_form)


@app.route("/delete/<int:film_id>")
def delete(film_id):
    film_to_delete = Movie.query.get(film_id)
    db.session.delete(film_to_delete)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
