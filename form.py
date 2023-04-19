from flask_wtf import FlaskForm
from wtforms import (HiddenField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    username = StringField('ユーザー名', validators=[
        DataRequired(message='ユーザー名が未登録です'),
        Length(max=10,message='ユーザー名は10文字までにして下さい')
    ])

    email = StringField('Eメールアドレス', validators=[
        Email(message='メールアドレスが未入力か、正しいアドレスではありません'),
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードを入力して下さい'),
    ])


class LoginForm(FlaskForm):
    email = StringField('Eメールアドレス', validators=[
        Email(message='メールアドレスが未入力か、正しいアドレスではありません'),
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードを入力して下さい'),
    ])


class PostForm(FlaskForm):
    title = StringField('記事タイトル', validators=[
        DataRequired(message='タイトルを入力して下さい'),
    ])
    content = TextAreaField('記事内容', validators=[
        DataRequired(message='記事内容を入力して下さい'),
    ],id='editor')
    update = SubmitField(label='更新する')
    delete = SubmitField(label='削除する')
    id = HiddenField()