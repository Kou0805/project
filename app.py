from crypt import methods
from email import message
import json
import sqlite3
from turtle import title
from webbrowser import get
from flask import Flask, render_template, request, session, redirect, g, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sample.sqlite3')
Base = declarative_base()
app = Flask(__name__)
#app.secret_key = b"random string..."

class Mydata(Base):
  __tablename__ = 'mydata'

  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  mail = Column(String(255))
  age = Column(Integer)

  #get dict data
  def toDict(self):
    return {
      'id':int(self.id),
      'name':str(self.name),
      'mail':str(self.mail),
      'age':int(self.age)
    }

#get list data
def getByList(arr):
  res = []
  for item in arr:
    res.append(item.toDict())
  return res

#get all mydata recode
def getAll():
  Session = sessionmaker(bind=engine)
  ses = Session()
  res = ses.query(Mydata).all()
  ses.close()
  return res

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html', title="Index", message ="SQlite Database",alert='データを追加してね',id=id)

@app.route('/ajax/', methods=['GET'])
def ajax():
  mydata = getAll()
  return jsonify(getByList(mydata));

@app.route('/form', methods=['post'])
def form():
  name = request.form.get('name')
  mail = request.form.get('mail')
  age = int(request.form.get('age'))
  mydata = Mydata(name=name, mail=mail, age=age)
  Session = sessionmaker(bind=engine)
  ses = Session()
  ses.add(mydata)
  ses.commit()
  ses.close()
  return 'ok'


# @app.route('/<id>', methods=["GET"])
# def index_id(id):
#   return render_template('index.html', title="INDEX", id=id,  message='sqlite3 database',alert = 'this is sqlite3 database')

# @app.route('/ajax/<id>', methods=['GET'])
# def ajax_id(id):
#   Session = sessionmaker(bind=engine)
#   ses=Session()
#   mydata = session.query(Mydata).filter(Mydata.id == id).one()
#   ses.close()
#   return jsonify(mydata.toDict());

# @app.route('/form/<id>', methods=["post"])
# def form_id(id):
#   name = request.form.get('name')
#   mail = request.form.get('mail')
#   age = int(request.form.get('age'))
#   Session = sessionmaker(bind=engine)
#   ses = Session()
#   mydata = ses.query(Mydata).filter(Mydata.id == id).one()
#   mydata.name = name
#   mydata.mail = mail
#   mydata.age = int(age)
#   ses.add(mydata)
#   ses.commit()
#   ses.close()
#   return 'ok'


if __name__ == '__main__':
  app.debug = True
  app.run(host='localhost')


