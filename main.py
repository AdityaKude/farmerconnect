from flask import Flask,render_template,request,session,redirect,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime


import stripe

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='adityakude'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/farmers'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))

class Farming(db.Model):
    fid=db.Column(db.Integer,primary_key=True)
    farmingtype=db.Column(db.String(100))


class Addagroproducts(db.Model):
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(100))
    productdesc=db.Column(db.String(300))
    price=db.Column(db.Integer)



class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    fid=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Register(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    farmername=db.Column(db.String(50))
    adharnumber=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    phonenumber=db.Column(db.String(50))
    address=db.Column(db.String(50))
    farming=db.Column(db.String(50))

# Payment model
class Payment(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    payment_gateway_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Expert Advice model
class ExpertAdvice(db.Model):
    __tablename__ = 'expertadvice'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user requesting advice
    query = db.Column(db.Text, nullable=False)       # User's query for advice
    status = db.Column(db.String(50), default='pending')  # Status of the advice request
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of the request

    def __repr__(self):
        return f'<ExpertAdvice {self.id} - {self.status}>'
    




# Initialize the database
db = SQLAlchemy()

class ExpertAdvice(db.Model):
    __tablename__ = 'expertadvice'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user requesting advice
    query = db.Column(db.Text, nullable=False)       # User's query for advice
    status = db.Column(db.String(50), default='pending')  # Status of the advice request
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of the request

    def __repr__(self):
        return f'<ExpertAdvice {self.id} - {self.status}>'

class ChatBot:
    def __init__(self):
        self.responses = {
            'how are you': 'I am doing great, thank you for asking!',
            'hello': 'Hi there! How can I assist you today?',
            'bye': 'Goodbye! Have a great day!',
        }
    
    def get_response(self, user_query):
        """
        Return a response based on the user's query. If no match is found, return a default response.
        """
        # Normalize the query to lowercase for case-insensitive matching
        user_query = user_query.lower()
        
        # Check if the query matches one of the predefined responses
        response = self.responses.get(user_query, 'I am sorry, I did not understand that. Could you please clarify?')
        
        return response

    def save_query(self, user_id, query):
        """
        Save the user's query to the database.
        """
        new_advice = ExpertAdvice(user_id=user_id, query=query, status='pending')
        db.session.add(new_advice)
        db.session.commit()

    def update_status(self, advice_id, status):
        """
        Update the status of a specific advice request in the database.
        """
        advice = ExpertAdvice.query.get(advice_id)
        if advice:
            advice.status = status
            db.session.commit()
            return f"Advice status updated to {status}."
        else:
            return "Advice not found."

# Example usage of ChatBot

# Initialize the chatbot
chatbot = ChatBot()





@app.route('/Expert Advice')
def expertadvice():
    return render_template('expertadvice.html')








# Route to view payments
@app.route('/payments')
def payments():
    return render_template('payments.html')


@app.route('/payments')
def view_payments():
    query = Payment.query.all()  # Fetch all payment records
    return render_template('payments.html', query=query)



@app.route('/payments/new', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        user_id = request.form['user_id']
        amount = request.form['amount']
        new_payment = Payment(user_id=user_id, amount=amount)
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment record created successfully!', 'success')
        return redirect(url_for('view_payments'))
    return render_template('add_payment.html')
 

@app.route('/payments/process/<int:payment_id>', methods=['GET'])
def process_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.payment_status = 'completed'
    payment.payment_gateway_id = 'MOCK12345678'  # Replace with real transaction ID if using a gateway
    db.session.commit()
    flash('Payment processed successfully!', 'success')
    return redirect(url_for('view_payments'))
   

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/farmerdetails')
@login_required
def farmerdetails():
    # query=db.engine.execute(f"SELECT * FROM `register`") 
    query=Register.query.all()
    return render_template('farmerdetails.html',query=query)

@app.route('/agroproducts')
@login_required
def agroproducts():
    # query=db.engine.execute(f"SELECT * FROM `addagroproducts`") 
    query=Addagroproducts.query.all()
    return render_template('agroproducts.html',query=query)

@app.route('/addagroproduct',methods=['POST','GET'])
@login_required
def addagroproduct():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        productname=request.form.get('productname')
        productdesc=request.form.get('productdesc')
        price=request.form.get('price')
        products=Addagroproducts(username=username,email=email,productname=productname,productdesc=productdesc,price=price)
        db.session.add(products)
        db.session.commit()
        flash("Product Added","info")
        return redirect('/agroproducts')
   
    return render_template('addagroproducts.html')

@app.route('/triggers')
@login_required
def triggers():
    # query=db.engine.execute(f"SELECT * FROM `trig`") 
    query=Trig.query.all()
    return render_template('triggers.html',query=query)

@app.route('/addfarming',methods=['POST','GET'])
@login_required
def addfarming():
    if request.method=="POST":
        farmingtype=request.form.get('farming')
        query=Farming.query.filter_by(farmingtype=farmingtype).first()
        if query:
            flash("Farming Type Already Exist","warning")
            return redirect('/addfarming')
        dep=Farming(farmingtype=farmingtype)
        db.session.add(dep)
        db.session.commit()
        flash("Farming Addes","success")
    return render_template('farming.html')




@app.route("/delete/<string:rid>",methods=['POST','GET'])
@login_required
def delete(rid):
    # db.engine.execute(f"DELETE FROM `register` WHERE `register`.`rid`={rid}")
    post=Register.query.filter_by(rid=rid).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","warning")
    return redirect('/farmerdetails')


@app.route("/edit/<string:rid>",methods=['POST','GET'])
@login_required
def edit(rid):
    # farming=db.engine.execute("SELECT * FROM `farming`") 
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        # query=db.engine.execute(f"UPDATE `register` SET `farmername`='{farmername}',`adharnumber`='{adharnumber}',`age`='{age}',`gender`='{gender}',`phonenumber`='{phonenumber}',`address`='{address}',`farming`='{farmingtype}'")
        post=Register.query.filter_by(rid=rid).first()
        print(post.farmername)
        post.farmername=farmername
        post.adharnumber=adharnumber
        post.age=age
        post.gender=gender
        post.phonenumber=phonenumber
        post.address=address
        post.farming=farmingtype
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/farmerdetails')
    posts=Register.query.filter_by(rid=rid).first()
    farming=Farming.query.all()
    return render_template('edit.html',posts=posts,farming=farming)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        print(username,email,password)
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        # encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=password)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","warning")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/register',methods=['POST','GET'])
@login_required
def register():
    farming=Farming.query.all()
    if request.method=="POST":
        farmername=request.form.get('farmername')
        adharnumber=request.form.get('adharnumber')
        age=request.form.get('age')
        gender=request.form.get('gender')
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        farmingtype=request.form.get('farmingtype')     
        query=Register(farmername=farmername,adharnumber=adharnumber,age=age,gender=gender,phonenumber=phonenumber,address=address,farming=farmingtype)
        db.session.add(query)
        db.session.commit()
        # query=db.engine.execute(f"INSERT INTO `register` (`farmername`,`adharnumber`,`age`,`gender`,`phonenumber`,`address`,`farming`) VALUES ('{farmername}','{adharnumber}','{age}','{gender}','{phonenumber}','{address}','{farmingtype}')")
        # flash("Your Record Has Been Saved","success")
        return redirect('/farmerdetails')
    return render_template('farmer.html',farming=farming)



@app.route('/')
def payment():
    return render_template('payment.html')



@app.route('/weather',methods=['POST','GET'])
@login_required
def weather():
    return render_template('weather.html')


@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'



app.run(debug=True)    