import atexit
import json
import re
import uuid
from pprint import pprint

from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, EmailStr, validator, ValidationError
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgresql://admin:admin@127.0.0.1:5431/flask_netology')

Base = declarative_base()
Session = sessionmaker(bind=engine)
app = Flask('server')
atexit.register(lambda: engine.dispose())

PASSWORD_REG = re.compile("^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,200}$")
#UUID_REG = re.compile('^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$')
UUID_REG = re.compile('^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


# PASSWORD_REG = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$')
# PASSWORD_REG = re.compile('^(?=[^\d_].*?\d)\w(\w|[!@#$%]){7,20}')


class HttpError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_mes = error_message


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value):
        if not PASSWORD_REG.search(value):
            raise ValueError('password  is shit')
        return value


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


class Ad(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)


class Token(Base):
    __tablename__ = "tokens"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, lazy="joined")


Base.metadata.create_all(engine)

bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.error_mes
    })
    response.status_code = error.status_code
    return response


@app.errorhandler(ValidationError)
def validation_error_handler(error: ValidationError):
    response = jsonify({
        'error': error.errors()
    })
    response.status_code = 400
    return response


def check_token(session):
    r = request.headers
    token = (
        session.query(Token)
        .join(User)
        .filter(
            User.email == request.headers.get("email"),
            Token.id == request.headers.get("token"),
        )
        .first()
    )
    if token is None:
        raise HttpError(401, "invalid token")
    return token


class UserView(MethodView):

    def get(self):
        with Session() as ses:
            # users = ses.query(User)
            # user_list = []
            # for user in users:
            #     user_list.append({'user_id': user.id,
            #                       'email': user.email,
            #                       'password': user.password,
            #                       'token': ses.query(Token)
            #                      .join(User)
            #                      .filter(User.id == user.id, )
            #                      .first()})
            # pprint(user_list)
            # return jsonify(user_list)
            users = ses.query(Token)
            user_list = []
            for user in users:
                user_list.append({'token_id': user.id,
                                  'creation_time': user.creation_time,
                                  'user_id': user.user_id})
            pprint(user_list)
            return jsonify(user_list)

    def post(self):
        json_data = request.json
        json_data_validated = UserCreateModel(email=json_data['email'], password=json_data['password']).dict()
        with Session() as ses:
            user = User(email=json_data_validated['email'], password=bcrypt.generate_password_hash(
                json_data_validated['password'].encode()).decode())
            token = Token(user=user)
            ses.add(user)
            ses.add(token)
            try:
                ses.commit()
                return jsonify({
                    'id': user.id,
                    'registration_time': user.registration_time.isoformat(),
                    'token':
                        ses.query(Token)
                        .join(User)
                        .filter(User.id == user.id, )
                        .first()
                })
            except IntegrityError:
                raise HttpError(400, 'user already exists')


class AdCreateModel(BaseModel):
    header: str
    description: str
    token: str

    @validator('description')
    def good_description(cls, value):
        if len(value) < 5:
            raise ValueError('description is too short')
        if len(value) > 255:
            raise ValueError('description is too long')

        return value

    @validator('header')
    def good_header(cls, value):
        if len(value) < 3:
            raise ValueError('header is too short')
        if len(value) > 35:
            raise ValueError('header is too long')

        return value

    @validator('token')
    def valid_token(cls, value):
        if not UUID_REG.search(value):
            raise ValueError('token is not valid')
        return value



class AvitoView(MethodView):

    def delete(self):
        pass

    def get(self):
        print('hello')
        return jsonify({'text': "hello"})

    def post(self):
        json_data = request.json
        json_data_validated = AdCreateModel(header=json_data['header'],
                                            description=json_data['description'],
                                            token=json_data['token']).dict()
        with Session() as ses:

            validate_token = (
                ses.query(Token)
                .filter(Token.id == json_data_validated['token'])
                .first()
            )
            if not validate_token:
                raise HttpError(401, "invalid token")

            ad = Ad(
                header=json_data_validated['header'],
                description=json_data_validated['description'],
                user_id=validate_token.user_id
            )
            ses.add(ad)
            try:
                ses.commit()
                return jsonify({
                    'id': ad.id,
                    'registration_time': ad.registration_time.isoformat(),
                    'description': ad.description
                })
            except IntegrityError:
                raise HttpError(400, 'ad already exists')


app.add_url_rule('/users/', view_func=UserView.as_view('create_user'), methods=['POST'])
app.add_url_rule('/users/', view_func=UserView.as_view('get_users'), methods=['GET'])
app.add_url_rule('/ads/', view_func=AvitoView.as_view('create_ad'), methods=['POST'])
app.add_url_rule('/ads/', view_func=AvitoView.as_view('get_ad'), methods=['GET'])
app.add_url_rule('/ads/', view_func=AvitoView.as_view('delete_ad'), methods=['DELETE'])

app.run(
    host='0.0.0.0',
    port=6000
)
