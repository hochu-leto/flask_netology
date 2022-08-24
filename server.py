import atexit
import json

from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://admin:admin@127.0.0.1:5431/flask_netology')

Base = declarative_base()
Session = sessionmaker(bind=engine)
flask = Flask('server')
atexit.register(lambda: engine.dispose())


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)


@flask.route('/test/', methods=['GET'])
def test():
    # return json.dumps({'status': 'OK'})
    return jsonify({'status': 'OK'})


flask.run(
    host='0.0.0.0',
    port=6000
)
