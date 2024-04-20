from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    address = db.Column(db.String(200))
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))


@app.route('/')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)


@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(
            name=request.form['name'],
            specialization=request.form['specialization'],
            address=request.form['address'],
            website=request.form['website'],
            phone=request.form['phone']
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:id>', methods=['POST'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    db.session.delete(restaurant)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if request.method == 'POST':
        restaurant.name = request.form['name']
        restaurant.specialization = request.form['specialization']
        restaurant.address = request.form['address']
        restaurant.website = request.form['website']
        restaurant.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', restaurant=restaurant)


@app.route('/search', methods=['POST'])
def search_restaurant():
    specialization = request.form['specialization']
    restaurants = Restaurant.query.filter_by(specialization=specialization).all()
    return render_template('search.html', restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True)
