from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(Form):
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
