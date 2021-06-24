from flask import Flask, redirect, render_template, url_for, request
import Predictor
app = Flask(__name__)


@app.route('/static/styles.css')
def cssStyle():
    print("CSS")
    return "static/styles.css"

@app.route('/')
def homePage():
    return render_template('/index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        myurl = request.form['url']
    else:
        myurl = request.args.get('url')

    result1, result2 ,result3= Predictor.predict(myurl)

    print(myurl, result1, result2, result3)

    if result1 == -1 and  result2 == -1 and result3 == -1:
        return render_template('/results_safe.html', url=myurl)
    else:
        return render_template('/results_unsafe.html', url=myurl)


if __name__ == "__main__":
    app.run(debug=True, port=8000)