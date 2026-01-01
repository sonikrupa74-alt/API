from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql

app = FastAPI()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="tops",
        cursorclass=pymysql.cursors.DictCursor
    )

class Emp(BaseModel):
    name: str
    salary: int

@app.get("/")
def home():
    return {"message": "FastAPI + MySQL is working successfully"}

@app.get("/employees")
def get_all_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    conn.close()
    return data

@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE emp_id=%s", (emp_id,))
    data = cur.fetchone()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="Employee not found")
    return data

@app.post("/employees")
def add_employee(emp: Emp):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO employees (e_name, e_salary) VALUES (%s, %s)",
        (emp.name, emp.salary)
    )
    conn.commit()
    emp_id = cur.lastrowid
    conn.close()
    return {"message": "Employee added successfully", "id": emp_id}

@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: Emp):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE employees SET e_name=%s, e_salary=%s WHERE emp_id=%s",
        (emp.name, emp.salary, emp_id)
    )

    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    conn.close()
    return {"message": "Employee updated successfully"}

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE emp_id=%s", (emp_id,))
    conn.commit()

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    conn.close()
    return {"message": "Employee deleted successfully"}
