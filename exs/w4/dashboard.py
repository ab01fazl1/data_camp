# imports
# TODO remove unused imports

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import text
import sqlalchemy.orm
from datetime import time, datetime

# start sql engine and connect
url_object = URL.create(
    "mysql+mysqlconnector",
    username="ab01fazl",
    password="P@ssAb01",
    host="localhost",
    database='imdb'
)

engine = create_engine(url_object)
session = Session(engine)

# Q3 - start
st.set_page_config(
    page_title='Part 3',
    # TODO change this
    page_icon=':snake:'
)
st.title("Quera Data Bootcamp Week4")


# Q3 P1 start
st.header("Filtering Tables")
"""
    select year and i will filter the DB for you
"""
# print(session.query('Movie').all())
# TODO get the min and max from DB
cursor.execute(text(<whatever_needed_to_be_casted>))
min_year = engine.
# min_year = session.query('Movie.year', func.max('Movie.year'))
max_year = session.query('Movie.year', func.min('Movie.year'))
def load_new_table():
    filtered_q = session.query('Movie.title').filter(v1 <= 'Movie.year' <= v2)
    st.table(filtered_q)

filtered_q = session.query('Movie.title').filter(min_year <= 'Movie.year' <= max_year)
st.table(filtered_q)

v1, v2 = st.slider(
    label="**use the slider:**",
    value=(min_year, max_year),
    on_change=load_new_table()
)


