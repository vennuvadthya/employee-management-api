import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def test_create_employee():
    """Test creating employees"""
    employees = [
        {
            "employee_id": "E123",
            "name": "John Doe",
            "department": "Engineering",
            "salary": 75000,
            "joining_date": "2023-01-15",
            "skills": ["Python", "MongoDB", "APIs"]
        },
        {
            "employee_id": "E124",
            "name": "Jane Smith",
            "department": "HR",
            "salary": 60000,
            "joining_date": "2023-02-01",
            "skills": ["Communication", "Management"]
        },
        {
            "employee_id": "E125",
            "name": "Bob Johnson",
            "department": "Engineering",
            "salary": 85000,
            "joining_date": "2023-03-10",
            "skills": ["Python", "React", "APIs"]
        }
    ]
    
    for emp in employees:
        response = requests.post(f"{BASE_URL}/employees", json=emp)
        print(f"Create Employee {emp['employee_id']}: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")

def test_get_employee():
    """Test getting employee by ID"""
    response = requests.get(f"{BASE_URL}/employees/E123")
    print(f"Get Employee E123: {response.status_code}")
    if response.status_code == 200:
        print(f"Employee: {response.json()}")

def test_update_employee():
    """Test updating employee"""
    update_data = {
        "salary": 80000,
        "skills": ["Python", "MongoDB", "APIs", "FastAPI"]
    }
    response = requests.put(f"{BASE_URL}/employees/E123", json=update_data)
    print(f"Update Employee E123: {response.status_code}")

def test_list_employees_by_department():
    """Test listing employees by department"""
    response = requests.get(f"{BASE_URL}/employees?department=Engineering")
    print(f"List Engineering Employees: {response.status_code}")
    if response.status_code == 200:
        employees = response.json()
        print(f"Found {len(employees)} Engineering employees")

def test_average_salary():
    """Test average salary by department"""
    response = requests.get(f"{BASE_URL}/employees/avg-salary")
    print(f"Average Salary: {response.status_code}")
    if response.status_code == 200:
        print(f"Salary Data: {response.json()}")

def test_search_by_skill():
    """Test searching employees by skill"""
    response = requests.get(f"{BASE_URL}/employees/search?skill=Python")
    print(f"Search by Python skill: {response.status_code}")
    if response.status_code == 200:
        employees = response.json()
        print(f"Found {len(employees)} employees with Python skill")

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    if response.status_code == 200:
        print(f"Health Status: {response.json()}")

if __name__ == "__main__":
    print("Testing Employee Management API...")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    print()
    
    # Create test employees
    print("Creating test employees...")
    test_create_employee()
    print()
    
    # Test other endpoints
    test_get_employee()
    print()
    
    test_update_employee()
    print()
    
    test_list_employees_by_department()
    print()
    
    test_average_salary()
    print()
    
    test_search_by_skill()
    print()
    
    print("Testing completed!")