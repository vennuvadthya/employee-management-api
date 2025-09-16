from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import motor.motor_asyncio
from bson import ObjectId
import os

# Initialize FastAPI app
app = FastAPI(title="Employee Management API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
database = client.assessment_db
employees_collection = database.employees

# Pydantic Models
class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique employee identifier")
    name: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=50)
    salary: float = Field(..., gt=0)
    joining_date: date
    skills: List[str] = Field(default_factory=list)

class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., description="Unique employee identifier")
    name: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=50)
    salary: float = Field(..., gt=0)
    joining_date: date
    skills: List[str] = Field(default_factory=list)

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=50)
    salary: Optional[float] = Field(None, gt=0)
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None

class AvgSalaryResponse(BaseModel):
    department: str
    avg_salary: float

# Helper function to convert MongoDB document to dict
def employee_helper(employee) -> dict:
    return {
        "employee_id": employee["employee_id"],
        "name": employee["name"],
        "department": employee["department"],
        "salary": employee["salary"],
        "joining_date": employee["joining_date"],
        "skills": employee["skills"]
    }

# 1. Create Employee
@app.post("/employees", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    # Check if employee_id is unique
    existing_employee = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing_employee:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    # Insert new employee
    employee_dict = employee.dict()
    result = await employees_collection.insert_one(employee_dict)
    
    # Return the created employee
    created_employee = await employees_collection.find_one({"_id": result.inserted_id})
    return Employee(**employee_helper(created_employee))

# 2. Get Employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Employee(**employee_helper(employee))

# 3. Update Employee
@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, employee_update: EmployeeUpdate):
    # Check if employee exists
    existing_employee = await employees_collection.find_one({"employee_id": employee_id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Prepare update data (only include fields that are not None)
    update_data = {}
    update_dict = employee_update.dict()
    for key, value in update_dict.items():
        if value is not None:
            update_data[key] = value
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Update employee
    await employees_collection.update_one(
        {"employee_id": employee_id}, 
        {"$set": update_data}
    )
    
    # Return updated employee
    updated_employee = await employees_collection.find_one({"employee_id": employee_id})
    return Employee(**employee_helper(updated_employee))

# 4. Delete Employee
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# 5. List Employees by Department
@app.get("/employees", response_model=List[Employee])
async def list_employees(department: Optional[str] = Query(None)):
    if department:
        # Filter by department and sort by joining_date (newest first)
        cursor = employees_collection.find({"department": department}).sort("joining_date", -1)
    else:
        # Get all employees
        cursor = employees_collection.find({})
    
    employees = await cursor.to_list(length=None)
    return [Employee(**employee_helper(emp)) for emp in employees]

# 6. Average Salary by Department
@app.get("/employees/avg-salary", response_model=List[AvgSalaryResponse])
async def average_salary_by_department():
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "department": "$_id",
                "avg_salary": {"$round": ["$avg_salary", 2]},
                "_id": 0
            }
        }
    ]
    
    result = await employees_collection.aggregate(pipeline).to_list(length=None)
    return [AvgSalaryResponse(**item) for item in result]

# 7. Search Employees by Skill
@app.get("/employees/search", response_model=List[Employee])
async def search_employees_by_skill(skill: str = Query(..., description="Skill to search for")):
    # Find employees who have the given skill in their skills array
    cursor = employees_collection.find({"skills": {"$in": [skill]}})
    employees = await cursor.to_list(length=None)
    return [Employee(**employee_helper(emp)) for emp in employees]

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Employee Management API - Assessment Task"}

# Health check
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        await database.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)