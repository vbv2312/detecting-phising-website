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
    result1,result2 = Predictor.predict(myurl)
    if result1 == 0:
        ans1 = "Legitimate"
    else:
        ans1 = "Phishing"

    if result2 == 0:
        ans2 = "Legitimate"
    else:
        ans2 = "Phishing"

    return "<div> <h1>Results</h1><h2>MY URL " +myurl+ " is :</h2><h2> Acc. to Model 1 :" + ans1 +"</h2><h2> Acc. to Model 2 :" + ans2 +"</h2></div>"


if __name__ == "__main__":
    app.run(debug=True)
