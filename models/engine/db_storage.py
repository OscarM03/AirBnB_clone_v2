#!/usr/bin/python3
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        obj_list = []

        if cls is None:
            obj_list = self.__session.query(State).all()
            obj_list.extend(self.__session.query(City).all())
            obj_list.extend(self.__session.query(User).all())
            obj_list.extend(self.__session.query(Place).all())
            obj_list.extend(self.__session.query(Review).all())
        else:
            obj_list = self.__session.query(cls).all()

        obj_dict = {}

        for obj in obj_list:
            cls_name = obj.__class__.__name__
            cls_id = obj.id
            key = "{}.{}".format(cls_name, cls_id)
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        ses = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses)
        self.__session = Session()

    def close(self):
        """Calls remove() on the private session attribute"""
        self.__session.close()
