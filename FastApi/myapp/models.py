from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from .database import Base

class TeachersModel(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, )
    email = Column(String, unique=True, )
    name = Column(String, )
    age = Column(Integer, )
    subject = Column(String, )
    class Config:
        orm_mode = True

class StudentsModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, )
    email = Column(String,unique=True,)
    name = Column(String, )
    std = Column(String, )
    age = Column(Integer, )
    # teacher_id = Column(Integer,ForeignKey("teachers.id"))
    class Config:
        orm_mode = True

class AssignTeacher(Base):
    __tablename__ = 'assignteachers'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer,ForeignKey("teachers.id"))
    student_id = Column(Integer,ForeignKey("students.id"))
    # class Config:
    #     orm_mode = True

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    last_login = Column(DateTime)


