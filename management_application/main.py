from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os





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
    db.Column('cart_id', db.Integer, db.ForeignKey('cart._id'), primary_key=True),
    db.Column('rental_id', db.Integer, db.ForeignKey('rental._id'), primary_key=True)
    )


class UserFactory():
    def makeSpecificUser(self, type, username, email, password, jobPosition=None):
        if type=="customer":
            return Customer(username, email, password)
        elif type=="employee":
            return Employee(username, email, password, jobPosition)

class User(UserMixin, db.Model):
    static_id = 1
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(15), unique=True)
    _email = db.Column(db.String(50), unique=True)
    _password = db.Column(db.String(80))
    type = db.Column(db.String(32))

    cart = db.relationship("Cart", backref='user', lazy=True, uselist=False)



    def __init__(self,username, email, password):
        self.id = User.static_id
        self._username = username;
        self._email = email;
        self._password = password;

        User.static_id += 1

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type,
    }

    def getCart(self):
        return self.cart;
    def getUsername(self):
        return self._username
    def getEmail(self):
        return self._email
    def getId(self):
        return self.id
    def getPassword(self):
        return self._password
    def getCurrentOrders(self):
        return self.currentOrders

    def setUsername(self, username):
        self._username = username
    def setEmail(self, email):
        self._email = email
    def setId(self, id):
        self.id = id
    def setPassword(self, password):
        self._password = password
    def setCart(self):
        self.cart = Cart(user = self)

    def isCustomer(self):
        pass


class Customer(User):
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    def __init__(self,username, email, password):
        super().__init__(username, email, password)
    def isCustomer(self):
        return True

class Employee(User):

    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }
    def __init__(self, username, email, password, jobPosition):
        super().__init__(username, email, password)
        self._jobPosition = jobPosition

    def isCustomer(self):
        return False


class Cart(db.Model):
    _id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    rentals = db.relationship('Rental', secondary='cart_with_items')

    def get_total_cost(self):
        total = 0
        for rental in self.rentals:
            total += rental.getCost()
        return total;



    def add_item(self,item):

        print(item._itemName)
        try:
            self.rentals.append(item)
            item._available -= 1
            db.session.commit()
            print(self.rentals)

        except:
            print("Couldn't add item into cart\n")

    def remove_item(self,item):
        try:
            item_to_be_removed = Rental.query.filter_by(_id=item).first()
            print(item_to_be_removed)
            self.rentals.remove(item_to_be_removed)

            item_to_be_removed._stock+=1
            db.session.commit()
        except:
            print("Couldn't remove item")

    def checkout(self):
        for item in self.rentals:

            self.rentals.remove(item)
            item.stock += 1;
        db.session.commit()







class Rental(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    _itemName = db.Column(db.String(15), unique=True);
    _itemCost = db.Column(db.Float)
    _itemImageUrl = db.Column(db.String(200))
    _stock = db.Column(db.Integer)
    type = db.Column(db.String(32))
    #foreign key is a primary key that refers to a key in another table
    __mapper_args__ = {
        'polymorphic_identity': 'rental',
        'polymorphic_on': type,
    }  #

    def __init__(self,item_id, item_name, item_cost, item_image_url,stock):
        self._id = item_id
        self._itemName = item_name
        self._itemCost = item_cost
        self._itemImageUrl = item_image_url
        self._stock = stock

    carts = db.relationship('Cart', secondary='cart_with_items')

    def getId(self):
        pass

    def getItemName(self):
        pass

    def getItemCost(self):
        pass

    def getItemImageUrl(self):
        pass

    def getItemStock(self):
        pass

    def getRentals():
        available_rentals = Rental.query.filter(Rental._stock>=1)
        return available_rentals


class Snowboard(Rental, db.Model):
    _boardLength = db.Column(db.Float)
    __mapper_args__ = {
        'polymorphic_identity': 'snowboard'
    }
    def __init__(self,item_id, item_name, item_cost, item_image_url,stock):
        self._id = item_id
        self._itemName = item_name
        self._itemCost = item_cost
        self._itemImageUrl = item_image_url
        self._stock = stock
        self._boardLength = 180

    def getId(self):
        return self._id

    def getItemName(self):
        return self._itemName

    def getItemCost(self):
        return self._itemCost

    def getItemImageUrl(self):
        return self._itemImageUrl

    def getStock(self):
        return self._Stock

    def getBoardLength(self):
        return self._boardLength

    def getRentals():
        available_rentals = Snowboard.query.filter(Snowboard._stock>=1)
        return available_rentals

    def setId(self, id):
        self._id = id

    def setItemName(self, name):
        self._itemName = name

    def setCost(self, cost):
        self._itemCost = cost

    def setItemImageUrl(self, url):
        self._itemImageUrl = url

    def setItemStock(self, stock):
        self._stock = stock

    def setBoardLength(self, length):
        self._boardLength = length

class Skis(Rental,db.Model):
    _skiLength = db.Column(db.Float)
    __mapper_args__ = {
        'polymorphic_identity': 'skis'
    }
    def __init__(self, id, item_name, item_cost, item_image_url, stock):
        #super().__init__(item_id, item_name, item_cost, item_image_url)
        self._id = id
        self._itemName = item_name
        self._itemCost = item_cost
        self._itemImageUrl = item_image_url
        self._stock = stock
        self._skiLength = 176



    def getId(self):
        return self._id

    def getItemName(self):
        return self._itemName

    def getItemCost(self):
        return self._itemCost

    def getSkiLength(self):
        return self._skiLength
    def getRentals():
        available_rentals = Skis.query.filter(Skis._stock>=1)
        return available_rentals

    def setId(self, id):
        self._id = id

    def setItemName(self, name):
        self._itemName = name

    def setCost(self, cost):
        self._itemCost = cost

    def setItemImageUrl(self, url):
        self._itemImageUrl = url

    def setItemStock(self, stock):
        self._stock = stock

    def setSkiLength(self, length):
        self._skiLength = length

class Boots(Rental, db.Model):
    _bootSize = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'boot'
    }


    def __init__(self,item_id, item_name, item_cost, item_image_url, stock):
        super().__init__(item_id, item_name, item_cost, item_image_url, stock)
        self._bootSize = 25


    def getId(self):
        return self._id

    def getItemName(self):

        return self._itemName

    def getCost(self):
        return self._itemCost

    def getUrl(self):
        return self._itemImageUrl

    def getBootSize(self):
        return self._bootSize

    def getRentals():
        available_rentals = Boots.query.filter(Boots._stock>=1)
        return available_rentals

    def setBootSize(self, size):
        self._bootSize = size






class RentalItemFactory():
    def __init__(self, id, itemName, itemCost, itemImageUrl, stock):
        self._id = id
        self._itemName = itemName
        self._itemCost = itemCost
        self._itemImageUrl = itemImageUrl
        self._stock = stock
    def makeSnowRental(self,newRentalType):
        if newRentalType == "Ski":
            return Skis(self._id, self._itemName, self._itemCost, self._itemImageUrl, self._stock);
        elif newRentalType == "Snowboard":
            return Snowboard(self._id, self._itemName, self._itemCost, self._itemImageUrl, self._stock);
        elif newRentalType == "Boots":
            return Boots(self._id, self._itemName, self._itemCost, self._itemImageUrl, self._stock)
        else:
            return None







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

class EmployeeRegisterForm(FlaskForm):
    #email field
    #password field
    #

    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=8, max=80)])
    jobPosition = StringField('Job Position', validators=[InputRequired(), Length(min=10, max=30)])


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm();
    if form.validate_on_submit():
        user = User.query.filter_by(_username=form.username.data).first()
        if user:
            if check_password_hash(user._password, form.password.data):
                session['username'] = form.username.data

                #redirect them to dashboard
                login_user(user, remember=form.remember.data)
                if(type(user) == Employee):
                    return redirect(url_for('employeeDashboard'))
                else:
                    return redirect(url_for('dashboard'))
        return '<h1> Invalid Username Or Password </h1>'
    return render_template("login.html", form=form)




@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm();
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = UserFactory()
        new_user = new_user.makeSpecificUser("customer", username = form.username.data, email = form.email.data, password = hashed_password)
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
            return '<h1> username or email already taken.</h1>'


    return render_template("signup.html", form = form)

@app.route("/employeeSignup", methods=['GET', 'POST'])
def employeeSignup():
    form = EmployeeRegisterForm();
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        # new_cart = Cart(user=new_user)
        new_user = UserFactory()
        new_user = new_user.makeSpecificUser("employee", username = form.username.data, email = form.email.data, password = hashed_password, jobPosition=form.jobPosition.data)
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
            return '<h1> username or email already taken.</h1>'
    return render_template("employeeSignup.html", form = form)





@app.route("/dashboard", methods = ['POST','GET'])
@login_required
def dashboard():

    if(current_user.type == "employee"):
        return redirect(url_for('employeeDashboard'))

    if request.method=='POST':
        #Return string name for selected rental item
        item_id = request.form.get('selected', False)
        if item_id:
            #Query the name of selected rental item
            try:
                new_cart_item = Rental.query.filter_by(_id=item_id).first()
                #rental 1
                current_user.cart.add_item(new_cart_item)

            except:
                print("couldn't find item")
        else:
            print("empty cart")

    available_rentals = Rental.getRentals()
    available_ski_rentals = Skis.getRentals()
    available_snowboard_rentals = Snowboard.getRentals()
    available_boot_rentals = Boots.getRentals()
    return render_template("dashboard.html", user=current_user, skis=available_ski_rentals, snowboards=available_snowboard_rentals, rental=available_rentals, boots=available_boot_rentals)

@app.route("/employeeDashboard", methods = ['POST', 'GET'])
@login_required
def employeeDashboard():

    if(current_user.type != "employee"):
        return redirect(url_for('dashboard'))

    if request.method=='POST':
        #Return string name for selected rental item
        item_id = request.form.get('selected', False)
        if item_id:
            #Query the name of selected rental item
            try:
                new_cart_item = Rental.query.filter_by(_id=item_id).first()
                #rental 1
                current_user.cart.add_item(new_cart_item)

            except:
                print("couldn't find item")
        else:
            print("empty cart")

    available_rentals = Rental.getRentals()
    available_ski_rentals = Skis.getRentals()
    available_snowboard_rentals = Snowboard.getRentals()
    available_boot_rentals = Boots.getRentals()

    return render_template("employeeDashboard.html", user=current_user, skis=available_ski_rentals, snowboards=available_snowboard_rentals, rental=available_rentals, boots=available_boot_rentals)

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
        temp_cart = request.form.get('order', False)

        if temp_cart=='1':
            print("Received Order Input")
            current_user.cart.checkout()
            return redirect(url_for('orderPlaced'))


    return render_template("checkout.html", user=current_user, name=current_user._username)



@app.route("/orderPlaced")
@login_required
def orderPlaced():
    return render_template("orderPlaced.html", user=current_user)


@app.route("/pastOrders")
@login_required
def pastOrders():
    return render_template("pastOrders.html", user=current_user)

#if we were to run our application with python, we will
#be able to run the application via python from app.run
if __name__ == '__main__':
    app.run(debug=True)
