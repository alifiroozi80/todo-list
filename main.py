from flask import Flask, render_template, request, redirect, url_for
import datetime
from wtforms import Form, StringField, validators
from flask_sqlalchemy import SQLAlchemy
import os

week_day = datetime.datetime.now().strftime("%A")
year = datetime.datetime.now().strftime("%Y")
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class AddForm(Form):
    text = StringField([validators.DataRequired()])


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Todos {self.text}>"


# db.create_all()


@app.route("/", methods=["POST", "GET"])
def home():
    form = AddForm()
    works = db.session.query(Todos).all()
    if request.method == 'POST' and form.validate():
        new_text = Todos(
            text=request.form["text"]
        )
        db.session.add(new_text)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("index.html", day=week_day, year=year, form=form, works=works)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    item_id = request.form["checkbox"]
    item_to_delete = Todos.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
