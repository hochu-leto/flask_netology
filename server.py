import atexit
import json

from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://admin:admin@127.0.0.1:5431/flask_netology')

Base = declarative_base()
Session = sessionmaker(bind=engine)
app = Flask('server')
atexit.register(lambda: engine.dispose())


class HttpError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_mes = error_message


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)


@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.message
    })
    response.status_code = 400
    return response


class UserView(MethodView):

    def get(self):
        pass

    def post(self):
        json_data = request.json
        with Session() as ses:
            user = User(email=json_data['email'], password=json_data['password'])
            ses.add(user)
            try:
                ses.commit()
                return jsonify({
                    'id': user.id,
                    'registration_time': user.registration_time.isoformat()
                })
            except IntegrityError:
                raise HttpError(400, 'user уже есть')



# @flask.route('/test/', methods=['GET'])
# def test():
#     # return json.dumps({'status': 'OK'})
#     return jsonify({'status': 'OK'})

app.add_url_rule('/users/', view_func=UserView.as_view('create_user'), methods=['POST'])

app.run(
    host='0.0.0.0',
    port=6000
)
