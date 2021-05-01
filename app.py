from flask import Flask, request
from markupsafe import escape
from flask import render_template
import pymssql 

#import google translator
from google_trans_new import google_translator

#panda csv files
#import numpy as np
import pandas as pd

app = Flask(__name__)
#conect MSSQL
conn = pymssql.connect(server='localhost', user='sa', password='myPassw0rd', database='tweets')
cursor = conn.cursor()
 
@app.route('/', methods=['GET', 'POST'])
def home():
  
  #cursor.execute("INSERT INTO Posts (title, created_at) VALUES ('Jorge tyls spend momeny','2023-03-03')")
  
  # make sure data inserted
  #row = conn.commit()

  # cursor.executemany(
  #   "INSERT INTO Posts (original_content, trans_content) VALUES (%s, %s)",
  #   [('John Smith', 'John Doe'),
  #    ('Jane Doe', 'Joe Dog'),
  #    ('Mike T.', 'Sarah H.')])
  # conn.commit()

  cursor.execute("SELECT * FROM posts")  

  row = cursor.fetchone() 
  #row = cursor.fetchall()
  
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
  df = pd.read_csv("multi_langues_dataset_10500.tsv", sep='\t')

  df = df.head(5)

  #limitar linhas e colunas [0:n -> linhas, [colunas]]
  #df = df.loc[:10, 2:3]

  dados = []

  df2 = pd.DataFrame(columns=('Date', 'Tweet'))

  # google translator
  translator = google_translator()

  for index, row in df.iterrows():
    translate_text = translator.translate(escape(row['Tweet']),lang_tgt='en')
    detect_src = translator.detect(row['Tweet'])
    detect_dest = translator.detect(translate_text)
    df2.loc[index] = [row['Tweet'], translate_text]
    dados.append((row['Tweet'],translate_text,detect_src[1], detect_dest[1], row['Tweet ID'], row['Date']))

    #cursor.execute(f"INSERT INTO Posts (original_content, trans_content, src, twitter_id, created_at) VALUES ('{row['Tweet']}',{translate_text}', '{detect_result}', '{row['Tweet ID']}', '{row['Date']}')")
    #row = conn.commit()
  cursor.executemany(
    "INSERT INTO Posts (original_content, trans_content, src, dest, tweeter_id, created_at) VALUES (%s, %s, %s, %s, %s, %s)", dados)

  conn.commit()
  conn.close()

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