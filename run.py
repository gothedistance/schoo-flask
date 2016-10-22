from flask import Flask, render_template, session, redirect, url_for, flash, abort
from form import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xNVg}f_m:UmiOB{9bC`SvB9j5N<-3I./' # CSRFトークン
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schoo.sqlite' # DBへのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def hash_password(original_pass):
    return generate_password_hash(original_pass)

def verify_password(hash_pass, original_pass):
    return check_password_hash(hash_pass, original_pass)

def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
            for column in model.__table__.columns)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def login(email, password):
        '''
        ログイン実行
        '''
        u = User.query.filter_by(email=email).first()
        if u and verify_password(u.password, password):
            return u
        return None


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String,nullable=True)
    publish_date = db.Column(db.DateTime,nullable=True, default=datetime.now)
    content = db.Column(db.Text,nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship('User')

@app.route("/")
def index():
    posts = [] # 非ログイン時
    if 'auth.user' in session:
        # ログインしているユーザーの記事だけを
        # 一覧で表示するようにしています
        posts = Post.query.filter(Post.user_id == session['auth.user']['id']).order_by(Post.publish_date.desc()).all()

    return render_template('index.html',posts=posts)


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


@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.login(form.email.data, form.password.data)
        if u is None:
            flash('ユーザー名とパスワードの組み合わせが違います。')
            return redirect(url_for('.login'))

        session['auth.user'] = get_model_dict(u)
        return redirect(url_for('.index'))

    return render_template(
        'login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))


@app.route("/add_post",methods=['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.id = None
        post.user_id = session['auth.user']['id']
        db.session.add(post)
        db.session.commit()

        flash('記事を公開しました！')
        return redirect(url_for(".index"))
    return render_template('add_post.html', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if not post:
        abort(404)

    return render_template('post.html',post=post)

@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    form = PostForm()
    if not post:
        abort(404)

    form.title.data = post.title
    form.content.data = post.content
    form.id.data = post.id

    return render_template('update_post.html',post=post,form=form)

@app.route('/update_post/',methods=['POST'])
def update_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post.query.filter(Post.id == form.id.data).first()
        if form.update.data:
            # 更新
            post.title = form.title.data
            post.content = form.content.data
            db.session.add(post)
            flash('記事内容を更新しました')
        else:
            # 削除
            db.session.delete(post)
            flash('記事を削除しました')

        db.session.commit()
        return redirect(url_for('.index'))

    return redirect(url_for('.show_post',post_id=form.id.data))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
