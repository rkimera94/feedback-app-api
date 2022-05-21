from crypt import methods
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return {'app': 'data'}


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():

    if request.method == 'POST':
        ratings = request.args.get('ratings')
        comment = request.args.get('comment')
        dealer = request.args.get('dealer')
        customer = request.args.get('customer')

        if not ratings or not comment or not dealer or not customer:
            message = 'Invalid Data requests'
            return {'status': 401, "message": message}
        else:
            data = {"customer": customer,
                    "ratings": ratings, "comment": comment, "dealer": dealer}
            message = "Data Loaded Successfully"
            return {'status': 200, "message": message, "data": data}


if __name__ == '__main__':
    app.debug = True
    app.run()
