from flask import Flask, render_template, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xNVg}f_m:UmiOB{9bC`SvB9j5N<-3I./'

@app.route("/")
def index():
    session['username'] = 'ここにあなたのお前を書いて下さい'
    return "Hello,World."

@app.route("/schoo")
def schoo():
    message = 'プログラミングを楽しんで下さい'
    return render_template('schoo.html',message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5200)
