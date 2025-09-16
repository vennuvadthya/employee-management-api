# Employee Management API 

A simple Employee Management API built with **FastAPI** and **MongoDB**.
It demonstrates CRUD operations, querying, and aggregation with clean JSON responses and API documentation via Swagger UI.

---

##  Features

* **CRUD APIs** – Create, Get, Update, Delete employees
* **Querying & Aggregation**

  * List employees by department (sorted by joining date)
  * Average salary by department (MongoDB aggregation)
  * Search employees by skill
* **Health Check API** – Verify database connection
* **CORS support** – Allow cross-origin requests
* **Interactive Docs** – Swagger UI available at `/docs`

---

## Tech Stack

* **FastAPI** (Python web framework)
* **MongoDB** (NoSQL database)
* **Motor** (async MongoDB driver)
* **Uvicorn** (ASGI server)

---

##  Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/employee-management-api.git
   cd employee-management-api
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

---

## Usage

* API runs on: `http://127.0.0.1:8000`
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔗 API Endpoints

### Employees

* `POST /employees` → Create new employee
* `GET /employees/{employee_id}` → Get employee by ID
* `PUT /employees/{employee_id}` → Update employee (partial updates supported)
* `DELETE /employees/{employee_id}` → Delete employee
* `GET /employees?department=Engineering` → List employees by department

### Aggregations & Search

* `GET /employees/avg-salary` → Average salary by department
* `GET /employees/search?skill=Python` → Search employees by skill

### Health Check

* `GET /health` → Check API and DB status

---

## Testing

Run the provided test script:

```bash
python test_api.py
```

This will test health check, CRUD operations, department listing, salary aggregation, and skill search.

---

##  Project Structure

```
employee-api-assignment/
│── main.py              # FastAPI app with all endpoints
│── test_api.py          # API testing script
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

---

## Notes

* Duplicate employee IDs during test runs will return `400 – already exists` (expected behavior).
* Ensure MongoDB is running locally on `mongodb://localhost:27017`.

---

##  Author

**Vennela**
