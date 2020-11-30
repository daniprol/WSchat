from flask import Flask, render_template

app = Flask(__name__)
# Secret key to sign the cookies in the flask sessions
# TODO: INCLUDE THIS KEY IN AN ENVIRONMENT VARIABLE
app.secret_key = 'replace later'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
