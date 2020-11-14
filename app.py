import requests
from flask import Flask, render_template, request, flash, redirect
import xml.etree.ElementTree as ET
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import DateForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fdsdff243213423g42jk3hg53k2j4fg53kj'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_code = db.Column(db.String(3))
    char_code = db.Column(db.String(3))
    nominal = db.Column(db.String(10))
    name = db.Column(db.String(50))
    value = db.Column(db.String(50))
    date = db.Column(db.String(15))

    def __repr__(self):
        return f"Name: {self.name}; Code: {self.char_code}; " \
               f"Nominal: {self.nominal}; Value: {self.value}"


@app.route('/', methods=["GET", "POST"])
def main():
    form = DateForm()
    dates = []
    for date in Course.query.all():
        if date.date not in dates:
            dates.append(date.date)

    if form.validate_on_submit():

        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={form.date.data}"
        res = requests.get(url)
        tree = ET.fromstring(res.text)
        for valute in tree.findall("Valute"):
            course = Course(num_code=valute.find("NumCode").text, char_code=valute.find("CharCode").text,
                            nominal=valute.find("Nominal").text, name=valute.find("Name").text,
                            value=valute.find("Value").text, date=form.date.data)
            db.session.add(course)
            db.session.commit()


        return redirect(f"/{form.date.data}")

    return render_template("index.html",
                           form=form,
                           course=Course.query.all(),
                           dates=dates)


@app.route('/<path:date>', methods=["GET", "POST"])
def date(date):
    return render_template("courses.html",
                           title=date,
                           course=Course.query.filter_by(date=date)
                           )


if __name__ == '__main__':
    app.run()
