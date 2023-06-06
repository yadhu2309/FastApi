from pydantic import BaseModel

class BasicDetails(BaseModel):
    name: str
    age: int
    email: str

class Teacher(BasicDetails):
    subject: str
 

class Student(BasicDetails):
    std: str
    admno: int
    rollno: int

class Users(BaseModel):
    username: str
    password: str
    