from flask import Flask, redirect, render_template, url_for, request
import Predictor

app = Flask(__name__)

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        myurl = request.form['url']
    else:
        myurl = request.args.get('url')

    print(myurl)
    result = Predictor.predict(myurl)
    if result == 0:
        ans = "Legitimate"
    else:
        ans = "Phishing"

    return "<h1>Results</h1><h2>MY URL " +myurl+ " is :</h2><h2>" + ans +"</h2>"


if __name__ == "__main__":
    app.run(debug=True)
