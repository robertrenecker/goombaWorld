from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import reduce
import os
import abc
import Checkout
#__name__ is special variable
app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
backref= db.backref
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.getcwd(), 'database.db')
))


cart_with_items = db.Table('cart_with_items',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('rental_id', db.Integer, db.ForeignKey('rental.id'), primary_key=True)
    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    cart = db.relationship("Cart", backref='user', lazy=True, uselist=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    rentals = db.relationship('Rental', secondary='cart_with_items')

    def get_total_cost(self):
        total = 0
        for rental in self.rentals:
            total += rental.getCost()
        return total;



    def add_item(self,item):

        print(item.item_name)
        try:


            self.rentals.append(item)
            item.available = 0
            db.session.commit()
            print(self.rentals)


        except:
            print('no')

    def remove_item(self,item):
        try:
            item_to_be_removed = Rental.query.filter_by(id=item).first()
            print(item_to_be_removed)
            self.rentals.remove(item_to_be_removed)

            item_to_be_removed.available=1
            db.session.commit()
        except:
            print("Couldn't remove item")




class Rental(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(15), unique=True);
    item_cost = db.Column(db.Float)
    item_image_url = db.Column(db.String(100))
    item_type = db.Column(db.String(50))
    available = db.Column(db.Integer)
    #foreign key is a primary key that refers to a key in another table

    carts = db.relationship('Cart', secondary='cart_with_items')

    def get_item_id():
        pass

    def getItemname():
        pass

    def getCost(self):
        return self.item_cost

    def getRentals():
        available_rentals = Rental.query.filter_by(available=1)
        return available_rentals


# class Snowboard(Rental):
#
#     def __init__(self,item_id, item_name, item_cost, item_image_url):
#         super().__init__(item_id, item_name, item_cost, item_image_url)
#
#

class Skis(Rental):

    def __init__(self, id, item_name, item_cost, item_image_url, stock):
        #super().__init__(item_id, item_name, item_cost, item_image_url)
        self.id = id
        self.item_name = item_name
        self.item_cost = item_cost
        self.item_image_url = item_image_url
        self.available = stock


    def get_item_id(self):
        return self.id

    def getItemname(self):
        return self.item_name

    def getCost(self):
        return self.item_cost




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    #email field
    #password field
    #

    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8, max=80)])

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                session['username'] = form.username.data

                #redirect them to dashboard
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1> Invalid Username Or Password </h1>'
    return render_template("login.html", form=form)




@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm();
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        new_cart = Cart(user=new_user)
        try:
            db.session.add(new_user)

            db.session.commit()
            try:
                db.session.add(new_cart)
                db.session.commit()
            except:
                return'<h1>Couldnt add cart</h1>'

            return redirect(url_for('dashboard'))
        except:
            return '<h1> username or email already taken.'


    return render_template("signup.html", form = form)




@app.route("/dashboard", methods = ['POST','GET'])
@login_required
def dashboard():
    print("The session is: %s \n\n\n"% session['username'])
    if request.method=='POST':
        #Return string name for selected rental item
        item_id = request.form.get('selected', False)
        if item_id:
            #Query the name of selected rental item
            try:
                new_cart_item = Rental.query.filter_by(id=item_id).first()
                current_user.cart.add_item(new_cart_item)

            except:
                print("couldn't find item")
        else:
            print("empty cart")

    available_rentals = Rental.getRentals()


    return render_template("dashboard.html", user=current_user, rental=available_rentals)

@app.route("/logout")
@login_required
def logout():
    logout_user();
    session.pop('username', None)
    session.pop('cart', None)
    return redirect(url_for('index'))


@app.route("/checkout", methods=['POST', 'GET'])
@login_required
def checkout():
    if request.method=='POST':
        item_id = request.form.get('remove', False)
        if item_id:

            current_user.cart.remove_item(item_id)
    return render_template("checkout.html", user=current_user, name=current_user.username)


    # session['cart'].get_total_of_cart();
    print("got total")

    return render_template("checkout.html", name=current_user.username)


#if we were to run our application with python, we will
#be able to run the application via python from app.run
if __name__ == '__main__':
    app.run(debug=True)
