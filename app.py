from crypt import methods
from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import connection_param


app = Flask(__name__)


ENV = 'dev'


if ENV == 'dev':
    username = connection_param['dev']['DB_USER']
    DB_HOST = connection_param['dev']['DB_HOST']
    DB_DATABASE_NAME = connection_param['dev']['DB_DATABASE_NAME']
    DB_PASS = connection_param['dev']['DB_PASS']
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{DB_PASS}@{DB_HOST}:5432/{DB_DATABASE_NAME}'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLAlchemy_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


# models
class FeedBack(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    comment = db.Column(db.Text)
    ratings = db.Column(db.String(200))

    def __init__(self, customer, dealer, comment, ratings):
        self.ratings = ratings
        self.customer = customer
        self.dealer = dealer
        self.comment = comment


@ app.route('/')
def index():
    return {'app': 'data'}


@ app.route('/submit-feedback', methods=['POST'])
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
            if db.session.query(FeedBack).filter(FeedBack.customer == customer).count() == 0:
                result = FeedBack(customer, dealer, comment, ratings)
                db.session.add(result)
                db.session.commit()

                data = {"customer": customer,
                        "ratings": ratings, "comment": comment, "dealer": dealer}
                message = "Data Loaded Successfully"
                return {'status': 200, "message": message, "data": data}
            else:
                message = 'You have already submitted Your feedback'
                return {'status': 401, "message": message}


if __name__ == '__main__':
    app.debug = True
    app.run()
