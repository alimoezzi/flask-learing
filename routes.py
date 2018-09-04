from flask import Flask, render_template, url_for,request,session,redirect
from models import db,User,Place
from forms import SignupForm,LoginForm,AddressForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:896@@localhost:5432/learningflask'
db.init_app(app)

app.secret_key = 'development-key'

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if 'email' in session:# used to avoid login page if user already login
        return redirect(url_for('home'))
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html',form=form)
        else:
            # adding the new user to db
            newuser = User(form.first_name.data,form.last_name.data,form.email.data,form.password.data)
            #fetch input data from form using data attribute
            db.session.add(newuser)
            db.session.commit()
            #initiating a new session
            session['email'] = newuser.email
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('signup.html',form=form)
    return 'Else'


@app.route("/home",methods=['GET','POST'])
# @app.route("/home/",methods=['GET','POST'])
#@app.route("/home/<id:int>")
def home(id=None):
    if 'email' not in session:# used to avoid login page if user already login
        return redirect(url_for('login'))
    # q = User.query.get(id)
    user = User.query.filter_by(email=session['email']).first()
    form = AddressForm()
    places= []
    my_coord = (37.4332,-122.0844)
    if request.method == 'POST':
        if form.validate()== False:
            return render_template("home.html",**dict(user=user,form=form))
        else:
            #get the add
            address =form.address.data
            #query for add
            p = Place()
            my_coord = p.address_to_latlang(address)
            places = p.query(address)

            # return those results
            return render_template('home.html',**dict(user=user,form=form,my_coord=my_coord,places=places))
    elif request.method == 'GET':
        return render_template("home.html",**dict(user=user,form=form,my_coord=my_coord,places=places))
    else:
        return "else"


@app.route("/logout")
def logout():
    session.pop('email',None)
    return redirect(url_for('login'))


@app.route("/login",methods=['GET','POST'])
def login():
    if 'email' in session:# used to avoid login page if user already login
        return redirect(url_for('home'))
    form =LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            # print('<script>alert("Data entered is not valid");</script>')
            return render_template('login.html',form=form)
        else:
            email = form.email.data
            password = form.password.data
            #checking if the user exists
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login',**{'id':user.uid}))
    elif request.method == 'GET':
        return render_template('login.html',form=form)
    return "else"

# @app.route("/message")
# def message(form):
    # return render_template('message.html',msg="Data entered is not valid")
    

if __name__ == "__main__":
    app.run(debug=True)
