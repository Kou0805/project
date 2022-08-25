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
from sqlalchemy.pool import SingletonThreadPool

engine = create_engine('sqlite:///read.sqlite3', echo=True, connect_args={"check_same_thread": False})
Base = declarative_base()
app = Flask(__name__)
#app.secret_key = b"random string..."

class Mydata(Base):
  __tablename__ = 'mydata'

  id = Column(Integer, primary_key=True)
  title = Column(String(255))
  author = Column(String(255))
  date = Column(String(255))
  content = Column(String(255))

  #get dict data
  def toDict(self):
    return {
      'id':int(self.id),
      'title':str(self.title),
      'author':str(self.author),
      'date':self.date,
      'content':str(self.content)
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
  return render_template('index.html', title="読書記録アプリ",alert='自分専用の読書記録をつけていこう！',id=id)

@app.route('/ajax/', methods=['GET'])
def ajax():
  mydata = getAll()
  return jsonify(getByList(mydata));

@app.route('/form', methods=['post'])
def form():
  title = request.form.get('title')
  author = request.form.get('author')
  date = request.form.get('date')
  content = request.form.get('content')
  mydata = Mydata(title=title, author=author, date=date,content=content)
  Session = sessionmaker(bind=engine)
  ses = Session()
  ses.add(mydata)
  ses.commit()
  ses.close()
  return 'ok'

if __name__ == '__main__':
  app.debug = True
  app.run(host='localhost')
