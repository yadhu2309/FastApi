from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from myapp.schemas import Teacher, Student, Users
from myapp import models
from sqlalchemy.orm import Session
from myapp.database import SessionLocal, engine
from datetime import datetime, timedelta
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import sessionmaker


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

session_timeout_minutes = 30
session_timeout_seconds = session_timeout_minutes * 60


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def helloWorld():
    print("hello world")
    return {'message':'Hello World'}

# create teachers
@app.post('/create_teacher/')
async def create_teacher(teacher: Teacher, db: Session = Depends(get_db)):
    data = models.TeachersModel(email=teacher.email, name=teacher.name, age=teacher.age, subject=teacher.subject)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# get teachers
@app.get('/teachers/')
async def teachers(db: Session = Depends(get_db)):
    return db.query(models.TeachersModel).all()

# get a teacher
@app.get('/teacher/{teacherId}')
async def teacher(teacherId: int, db: Session = Depends(get_db)):
    
    user_data = db.query(models.TeachersModel).filter(models.TeachersModel.id == teacherId).first()
    if not user_data:
        raise HTTPException(status_code=404, detail='User not found')
    return user_data


# update teacher details
@app.put('/teacher/{teacherId}/')
async def update_teacher(teacherId: int, updated_teacher: Teacher, db: Session = Depends(get_db)):
    user_data = db.query(models.TeachersModel).filter(models.TeachersModel.id == teacherId).first()
    if not user_data:
        raise HTTPException(status_code=404, detail='User not found')
    user_data.name = updated_teacher.name
    user_data.age = updated_teacher.age
    user_data.subject = updated_teacher.subject
    db.commit()

    return {'message':'User updated successfully'}
    
# delete teacher
@app.delete('/delete_teacher/{teacherId}/')
async def deleter_teacher(teacherId: int, db: Session = Depends(get_db)):
    user_data = db.query(models.TeachersModel).filter(models.TeachersModel.id == teacherId).first()
    if not user_data:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(user_data)
    db.commit()
    return {'message':'User deleted successfully'}

# create a student
@app.post('/create_student/')
async def create_student(student: Student, db: Session = Depends(get_db)):
    data = models.StudentsModel(email=student.email, name=student.name, age=student.age, std=student.std)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# get a student
@app.get('/students/')
async def students(db: Session = Depends(get_db)):
    return db.query(models.StudentsModel).all()

# update student
@app.put('/update_student/{studentId}/')
async def update_student(studentId: int,student:Student, db: Session = Depends(get_db)):

    user_data = db.query(models.StudentsModel).filter(models.StudentsModel.id == studentId).first()
    if not user_data:
        raise HTTPException(status_code=404, detail='Student not found')
    user_data.name = student.name
    user_data.age = student.age
    user_data.std = student.std
    db.commit()
    return {'message':'Student updated successfully'}
    
# delete student
@app.delete('/delete_student/{studentId}/')
async def delete_student(studentId: int, db: Session = Depends(get_db)):
    user_data = db.query(models.StudentsModel).filter(models.StudentsModel.id == studentId).first()
    if not user_data:
        raise HTTPException(status_code=404, detail='Student not found')
    db.delete(user_data)
    db.commit()
    return {'message':'Student deleted successfully'}

# assign students to teacher
@app.post('/teachers/{teacherId}/assign_students/{studentId}')
async def assign_students(teacherId: int, studentId: int, db: Session = Depends(get_db)):
    teacher_data = db.query(models.TeachersModel).filter(models.TeachersModel.id == teacherId).first()
    student_data = db.query(models.StudentsModel).filter(models.StudentsModel.id == studentId).first()

    if not (teacher_data):

        raise HTTPException(status_code=404, detail='Teacher not found')
    if not (student_data):

        raise HTTPException(status_code=404, detail='Student not found')
    assign_students_data = models.AssignTeacher(teacher_id=teacher_data.id,student_id=student_data.id)
    db.add(assign_students_data)
    db.commit()
    db.refresh(assign_students_data)

    return {'message':'Successfully '}



# 2. WAP using FastAPI web framework using either MongoDb or any SQL

# create user
@app.post('/user/')
async def user_create(user: Users, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == user.username).first()
    # print(user_data.username)
    if user_data:
        raise HTTPException(status_code=400, detail='User already exists')
    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# get user
def get_user(creadentials: HTTPBasicCredentials = Depends(security),db: Session = Depends(get_db)):
    username = creadentials.username
    password = creadentials.password

    user = db.query(models.User).filter(models.User.username == username).first()
    if user and password == user.password:
        return username
    raise HTTPException(status_code=401, detail="Invalid Username or Password")


# login user
@app.post('/login/')
async def user_login(response: JSONResponse, username: str = Depends(get_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    user.last_login = datetime.now()
    db.commit()
 
    response.set_cookie(
        key="session_token",
        value=username,
        max_age=session_timeout_seconds

    )

    return {"message": "Logged in successfully"}

# logout user
@app.get('/logout')
async def logout(response: JSONResponse):
    response.delete_cookie(key='session_token')
    return {'message':'Logged out successfully'}

# @app.middleware('http')
# async def session_timeout(request: Request, call_next, db: Session = Depends(get_db)):
#     session_token = request.cookies.get("session_token")
#     if session_token:
#         username = session_token
#         user = db.query(models.User).filter(models.User.username == username).first()
#         if user.last_login and datetime.now() - user.last_login > timedelta(seconds=session_timeout_seconds):
#              print("yadhu")
#              raise HTTPException(
#                 status_code=401,
#                 detail="Session timeout Please log in again"
#                 )


#     response = await call_next(request)
#     return response

    


#  3. WAP using FastAPI web framework 

# two latitude and longitude and give distance between them 
@app.post('/distance/twopoints/')
async def distance_btw_two_points(x2:int, x1:int, y1:int, y2:int):
    if not(x2 or x1 or y2 or y1):
        raise HTTPException(status_code=404, detail='Please provide x1, x2, y1, y2')
    d=((x2-x1)**2)+((y2-y1)**2)

    return {'distance':d**(1/2)}
