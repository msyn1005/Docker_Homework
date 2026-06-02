from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

@app.get("/courses")
def get_courses():
    if not os.path.exists("courses.json"):
        return []
    with open("courses.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/courses")
def create_course(course: Course):
    try:
        if not os.path.exists("courses.json"):
            with open("courses.json", "w", encoding="utf-8") as f:
                json.dump([], f)

        with open("courses.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        data.append({
          "course_name": course.course_name,
          "year": course.year,
          "semester": course.semester,
          "grade": course.grade
        })

        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"message": "수강기록이 성공적으로 추가되었습니다.", "inserted": course}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
