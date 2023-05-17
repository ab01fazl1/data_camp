'''
NOTE:
    I didn't make bidirectional relationships because it wasn`t mentioned anywhere in the Q box
'''

# imports
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, Text, VARCHAR
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import json

# db name
DB_NAME = 'imdb'

# replace this with your username and pass
# my user has full access
url_object = URL.create(
    "mysql+mysqlconnector",
    username="ab01fazl",
    password="P@ssAb01",
    host="localhost",
)

# crete my DB named imdb
engine = create_engine(url_object)
with engine.connect() as conn:
    conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    conn.execute(text(f"CREATE DATABASE {DB_NAME}"))

# new url to connect to DB
url_object = URL.create(
    "mysql+mysqlconnector",
    username="ab01fazl",
    password="P@ssAb01",
    host="localhost",
    database=DB_NAME
)

# initiate engine
engine = create_engine(url_object)

# create Base class
class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movie"

    # columns
    id: Mapped[int] = mapped_column(VARCHAR(8), primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(128))
    year: Mapped[int] = mapped_column(Integer)
    runtime: Mapped[int] = mapped_column(Integer)
    parental_guide: Mapped[str] = mapped_column(VARCHAR(8))
    gross_us_canada: Mapped[int] = mapped_column(Integer, nullable=True)


class Storyline(Base):
    __tablename__ = 'storyline'
    id: Mapped[int] = mapped_column(ForeignKey("movie.id"), primary_key=True)
    content: Mapped[str] = mapped_column(Text)

class Person(Base):
    __tablename__ = 'person'
    id: Mapped[int] = mapped_column(VARCHAR(8), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(32))

class Cast(Base):
    __tablename__ = 'cast'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))

class Crew(Base):
    __tablename__ = 'crew'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    role: Mapped[str] = mapped_column(VARCHAR(8))

class Genre(Base):
    __tablename__ = 'genre'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    genre: Mapped[str] = mapped_column(VARCHAR(16))

# save tables
Base.metadata.create_all(engine)

#                        it works fine till here by the looks of it

# create session and start populating DB
session = Session(engine)

# start populating
# open the json file -> loop through it


# person is stars, writers and directors
# they are list of dictionaries with mapping actor name to its id
# im combining the parsing of person with stars, writers and directors
def add_person(ls, role):
    for x in ls:
        for key in x:
            # add person
            # checking if person exists
            q = session.query(Person.id).filter(Person.id == x[key])
            if session.query(q.exists()).scalar() == False:
                    p = Person(id=x[key], name=key)
                    session.add(p)
                    session.commit()
            if role == 'stars':
                ca = Cast(movie_id=movie['id'], person_id=x[key])
                session.add(ca)
                session.commit()
            if role == 'writer' or role == 'director':
                cr = Crew(movie_id=movie['id'], person_id=x[key], role=role)
                session.add(cr)
                session.commit()


# Opening JSON file
f = open('data.json')
data = json.load(f)
for movie in data:

    # parental_guide
    if movie.get("parental_guide") is None or movie['parental_guide'] == 'Not Rated':
        movie['parental_guide'] = 'Unrated'

    m = Movie(id=movie['id'],
              title=movie['title'],
              year=movie['year'],
              runtime=movie['runtime'],
              parental_guide=movie['parental_guide'],
              gross_us_canada=movie['gross_us_canada'])
    session.add(m)
    session.commit()

    # parse genre because its a list
    for g in movie['genre']:
        gm = Genre(movie_id=movie['id'], genre=g)
        session.add(gm)
        session.commit()

    add_person(movie['stars'], role='stars')
    add_person(movie['director'], role='director')
    add_person(movie['writers'], role='writer')

    # story
    st = Storyline(id=movie['id'], content=movie['story'])
    session.add(st)
    session.commit()

# save
session.commit()

# Closing file
f.close()




