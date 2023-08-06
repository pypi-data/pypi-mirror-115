import os
from pathlib import Path
import datetime

from sqlalchemy import Column, ForeignKey, Integer, Float, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from appdirs import user_data_dir

def get_user_data_dir():
    appauthor = "joajfreitas"
    appname = "marcador"

    return user_data_dir(appname, appauthor)

def get_db_path():
    return Path(get_user_data_dir()) / Path("marcador.sqlite")

Base = declarative_base()

class Bookmark(Base):
    __tablename__ = 'bookmark'
    url = Column(String, primary_key=True)
    description = Column(String)
    count = Column(Integer)
    thumbnail = Column(String)
    score = Column(Float)
    creation_date = Column(Date)
    last_acessed_date = Column(Date)

    def deserialize(data):
        return Bookmark(
            url=data.get('url') or "",
            description=data.get('description') or "",
            count=data.get('count') or 0,
            thumbnail=data.get('thumbnail') or "",
            score=data.get('score') or 1.0,
            creation_date = data.get("creation_date"),
            last_acessed_date = data.get("last_acessed_date")
        )

    def serialize(self):
        return {
            "type": "bookmark",
            "url": self.url,
            "description": self.description,
            "count": self.count,
            "thumbnail": self.thumbnail,
            "score": self.score,
            "creation_date": str(self.creation_date),
            "last_acessed_date": str(self.last_acessed_date),
        }

    def __repr__(self):
        return f"Bookmark {{{self.creation_date=}, {self.url=}, {self.score=}}}"

class Tag(Base):
    __tablename__ = 'tag'

    #identifier = Column(Integer, primary_key = True)
    tag = Column(String, primary_key=True)

    def deserialize(data):
        assert data.get('tag') is not None

        return Tag(
            tag=data.get('tag'),
        )

    def serialize(self):
        return {
            "type": "tag",
            "tag": self.tag,
        }

    def __repr__(self):
        return f"Tag {{{self.tag=}}}"

class BookmarkTag(Base):
    __tablename__ = 'bookmark_tag'

    url = Column(String, ForeignKey('bookmark.url'), primary_key=True)
    tag = Column(String, ForeignKey('tag.tag'), primary_key=True)

    def deserialize(data):
        assert data.get('tag') is not None

        return BookmarkTag(
            tag=data.get('tag'),
            url=data.get('url')
        )

    def serialize(self):
        return {
            "type": "bookmark_tag",
            "tag": self.tag,
            "url": self.url,
        }

    def __repr__(self):
        return f"BookmarkTag {{bookmark={self.bookmark},tag={self.tag}}}"


def get_session(db_path: Path) -> Session:
    engine = create_engine("sqlite:///"+str(db_path))
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session: Session = DBSession()

    return session

class Core():
    def __init__(self, session):
        self.session = session

    def list(self):
        return self.session.query(Bookmark).order_by(Bookmark.score.desc()).all()

    def tags(self):
        return self.session.query(Tag).all()

    def bookmark_tags(self, url):
        return self.session.query(BookmarkTag).filter(BookmarkTag.url == url)

    def add(self, url):
        bookmark = Bookmark(
            url=url,
            score = 1,
            count = 1,
            creation_date = datetime.datetime.now(),
            last_acessed_date = datetime.datetime.now())

        self.session.add(bookmark)
        self.session.commit()

        return

    def add_tag(self, url, tag):
        book_tag = BookmarkTag(url=url, tag=tag)
        self.session.merge(book_tag)
        tag = Tag(tag=tag)
        self.session.merge(tag)
        self.session.commit()

    def delete(self, url):
        self.session.query(Bookmark).filter(Bookmark.url == url).delete()
        tags = self.session.query(BookmarkTag).filter(BookmarkTag.url == url).all()
        for tag in tags:
            self.session.query(Tag).filter(Tag.tag == tag.tag).delete()
        self.session.query(BookmarkTag).filter(BookmarkTag.url == url).delete()
        self.session.commit()

    def open(self, url):
        for bookmark in self.session.query(Bookmark).filter(Bookmark.url == url).all():
            bookmark.last_accessed_data = datetime.datetime.now()
            bookmark.count += 1


