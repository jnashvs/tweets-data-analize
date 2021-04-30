from flask import Flask, request
from markupsafe import escape
from flask import render_template
import pymssql 

#import google translator
from google_trans_new import google_translator

#panda csv files
#import numpy as np
import pandas as pd


## google translator atributes
url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

app = Flask(__name__)
#conect MSSQL
 
@app.route('/', methods=['GET', 'POST'])
def home():
  conn = pymssql.connect(server='localhost', user='sa', password='myPassw0rd', database='tweets')
  cursor = conn.cursor()
  #cursor.execute("SELECT * FROM posts")  
  cursor.execute("INSERT INTO Posts (title, created_at) VALUES ('Jorge tyls spend momeny','2023-03-03')")
  
  # make sure data inserted
  row = conn.commit()

  cursor.execute("SELECT * FROM posts")  

  #row = cursor.fetchone() 
  row = cursor.fetchall()
  
  conn.close()

  return render_template('home.html', row=row)

@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

## import panda
@app.route('/panda', methods=("POST", "GET"))
def html_table():
  file = 'tweets.csv'
  df = pd.read_csv(file)

  df = df.head(10)

  #df = df.loc[:10, ['author', 'content']]

  df2 = pd.DataFrame(columns=('author', 'content'))

  # google translator
  translator = google_translator()

  for index, row in df.iterrows():
    translate_text = translator.translate(escape(row['content']),lang_tgt='pt')
    df2.loc[index] = [row['author'], translate_text]

  #return df.to_html(header="true", table_id="table")
  return render_template('panda.html',  tables=[df2.to_html(classes='data')], titles=df2.columns.values)

@app.route('/translate/<text>', methods=("POST", "GET"))
def translate(text):
  translator = google_translator()  

  #for
  translate_text = translator.translate(escape(text),lang_tgt='en')  
  
  return translate_text

## NOT FOUND ERROR PAGE
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404