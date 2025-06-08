from flask import Flask, render_template, redirect, session, url_for, flash
from forms import LoginForm, Task
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.mutable import MutableList
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://python123:Python896%40@python123.mysql.pythonanywhere-services.com/python123$users_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
task_id = 1

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    task = db.Column(MutableList.as_mutable(db.JSON))

    def __repr__(self):
        return f"User({self.id}, '{self.username}')"

try:
    app_context = app.app_context()
    app_context.push()
    db.create_all()
except Exception as e:
    print("Some error occured: ", e)

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" not in session:
        return redirect(url_for('login'))
    else:
        global task_id
        form = Task()
        user = User.query.filter_by(username=session['username']).first()

        if form.validate_on_submit():
            task = form.enter_task.data
            if user.task is None:
                user.task = []

            user.task.append({"name":task, "task_id":task_id})
            task_id += 1

            db.session.commit()
            print(user.task)

            return redirect(url_for('home'))

        return render_template('index.html', form=form, title="Home", tasks=user.task)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    else:
        form = LoginForm()

        if form.validate_on_submit():
            # fetch the username and password from login form
            username = form.username.data
            password = form.password.data

            # check whether the user exists in database or not
            db_user = User.query.filter_by(username=username).first()

            # add user details in the database
            if db_user == None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                # create the session of the new user
                session['user_id'] = user.id
                session['username'] = username
            else:
                # user already exists
                if check_password_hash(db_user.password, password):
                    session['user_id'] = db_user.id
                    session['username'] = username
                else:
                    flash('Username already exists!')
                    return redirect(url_for('login'))

            # redirect the user to the homepage
            return redirect(url_for("home"))
        
        return render_template("login.html", title="Login", form = form)

@app.route("/logout")
def logout():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        # clear the session and redirect to login page
        session.clear()
        return redirect(url_for('login'))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_task(index):
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        user = User.query.filter_by(username=session["username"]).first()
        for task in user.task:
            if task['task_id'] == index:
                user.task.remove(task)
                db.session.commit()
                break

        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
