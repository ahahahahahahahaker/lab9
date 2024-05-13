from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Бибиков Дмитрий Вариант 3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Town_visiting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Town{self.id}. You visited {self.town} on {self.visit_date}'


@app.route('/')
def main():
    cities = Town_visiting.query.all()
    return render_template('index.html', cities_list=cities)


# для БД
@app.route('/add', methods=['POST'])
def add_town():
    data = request.json
    town = Town_visiting(**data)
    db.session.add(town)
    db.session.commit()


# для очистки
@app.route('/delete')
def drop_date():
    for city in Town_visiting.query.all():
        db.session.delete(city)
    db.session.commit()
    return redirect(url_for('main'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
