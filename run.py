from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from form import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xNVg}f_m:UmiOB{9bC`SvB9j5N<-3I./' # CSRFトークン
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/schoo.sqlite' # DBへのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def hash_password(original_pass):
    return generate_password_hash(original_pass)

def verify_password(hash_pass, original_pass):
    return check_password_hash(hash_pass, original_pass)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    publish_date = db.Column(db.DateTime,nullable=False)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/Hello")
def hello():
    return "Hello,World."


@app.route("/schoo")
def schoo():
    message = 'プログラミングを楽しんで下さい'
    return render_template('schoo.html',message=message)


@app.route("/signup",methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u:
            flash('そのメールアドレスは既に利用されています。')
            return redirect(url_for('.signup'))

        user = User()
        form.populate_obj(user)
        user.password = hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ユーザー登録が完了しました。ログインして下さい')
        return redirect(url_for(".signup"))

    return render_template('signup.html',form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5200)
