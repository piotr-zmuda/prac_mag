from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)

load_dotenv()

open_ai_key = os.getenv('OPEN_AI_KEY')
groq_key = os.getenv('GROQ_KEY')

mydb = mysql.connector.connect(
  host="admin",
  user="admin",
  password="your_password",
  database="prac_mag"
)
cursor = mydb.cursor()


def init_database(user:str, password: str, host:str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

db = init_database("admin","admin","localhost","3306","prac_mag")

# Example: Restricting CORS to specific origins and headers
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}}, headers=['Content-Type'])


def get_sql_chain(db):
    template = """
    Question: Tell me which team is going to win given the statistic?

    <TABLES>{columns}</TABLES>
    """
    prompt = ChatPromptTemplate.from_template(template)

    #llm = ChatOpenAI(api_key=open_ai_key)

    llm = ChatGroq(model="Llama3-70b-8192",temperature=0, api_key=groq_key)

    def get_schema(_):
        print(db.get_table_info())
        return db.get_table_info()
    return(
        RunnablePassthrough.assign(columns=get_schema)
        | prompt 
        | llm
        | StrOutputParser()
    )


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "Hello from Flask!",
        "items": [1, 2, 3, 4, 5]
    }
    return jsonify(data)

@app.route('/api/products', methods=['GET'])
def get_products():
    data = cursor.execute("SELECT * FROM PRODUCT;")
    rows = cursor.fetchall()
    thing_to_add = ""
    # Print the results
    for row in rows:
        thing_to_add+=str(row)+"\n"
    return jsonify(thing_to_add);  

@app.route('/api/generateAI', methods=['GET'])
def get_response_from_ai():
    user_query = request.args.get('user_query')
    chat_history = request.args.get('chat_history')
    sql_chain = get_sql_chain(db)
    response = sql_chain.invoke({
        "question": user_query,
    })
    sql_get = response
    cursor.execute(sql_get)
    rows = cursor.fetchall()
    thing_to_add = ""
    # Print the results
    for row in rows:
        thing_to_add+=str(row)
    return jsonify(response);  

if __name__ == '__main__':
    app.run(debug=True)


