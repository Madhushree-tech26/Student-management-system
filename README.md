# Student Management System

A simple web-based Student Management System built using Flask, SQLite, HTML, CSS, JavaScript, and Bootstrap.

This application allows users to add, view, search, update, and delete student records.

## Features

- Add new student records.
- Display all student records.
- Search students by name, email, department, or phone number.
- Edit existing student details.
- Delete student records.
- Validate required fields.
- Validate email addresses.
- Validate 10-digit phone numbers.
- Validate student year from 1 to 4.
- Prevent duplicate email addresses.
- Responsive user interface.
- SQLite database integration.
- REST API endpoints for student records.

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Jinja2
- Gunicorn
- Git and GitHub

## Project Structure

```text
Student-management-system/
│
├── app.py
├── README.md
├── requirements.txt
├── Procfile
├── .gitignore
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── base.html
    ├── index.html
    └── edit.html
```

## Database Structure

The application uses a SQLite database named `students.db`.

The `students` table contains the following fields:

| Field | Description |
|---|---|
| id | Unique student ID |
| name | Student full name |
| email | Student email address |
| phone | Student phone number |
| department | Student department |
| year | Student academic year |
| address | Student address |
| created_at | Record creation date and time |

## Requirements

Install the following software before running the project:

- Python 3
- VS Code
- Git
- A web browser

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/Madhushree-tech26/Student-management-system]
```

### 2. Open the project folder

```bash
cd student-management-system
```

### 3. Create a virtual environment

On Windows:

```bash
python -m venv venv
```

### 4. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 5. Install the required packages

```bash
python -m pip install -r requirements.txt
```

## Run the Application

Start the Flask application:

```bash
python app.py
```

Open the following address in a browser:

```text
http://127.0.0.1:5000
```

## How to Use

### Add a student

1. Enter the student's name.
2. Enter the student's email.
3. Enter a 10-digit phone number.
4. Select the department.
5. Select the academic year.
6. Enter the address.
7. Click **Add Student**.

### View students

All saved students appear in the Student Records table on the home page.

### Search students

Enter a name, email, department, or phone number in the search box and click **Search**.

### Edit a student

1. Click the **Edit** button.
2. Modify the student information.
3. Click **Save Changes**.

### Delete a student

1. Click the **Delete** button.
2. Confirm the deletion.

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/students` | Get all students |
| POST | `/api/students` | Create a student |
| GET | `/api/students/<id>` | Get one student |
| PUT | `/api/students/<id>` | Update a student |
| DELETE | `/api/students/<id>` | Delete a student |

## Example API Request

### Create a student

```http
POST /api/students
Content-Type: application/json
```

Request body:

```json
{
    "name": "Anitha Kumar",
    "email": "anitha@example.com",
    "phone": "9876543210",
    "department": "Computer Science",
    "year": 2,
    "address": "Coimbatore, Tamil Nadu"
}
```

## Validation

The application applies the following validation rules:

- Student name cannot be empty.
- Email address must use a valid format.
- Phone number must contain exactly 10 digits.
- Department is required.
- Year must be between 1 and 4.
- Email addresses must be unique.
- Server-side validation is applied before saving data.

## Run with Gunicorn

For deployment, use:

```bash
gunicorn app:app
```

The `Procfile` contains:

```text
web: gunicorn app:app
```

## Deployment

This project can be deployed using Render or another Python-compatible hosting service.

Use the following Render settings:

```text
Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app
```

After deployment, Render provides a public website URL.

## Testing

The following operations should be tested:

- Add a student with valid information.
- Submit the form with missing information.
- Enter an invalid email address.
- Enter an invalid phone number.
- Add a duplicate email address.
- Search for a student.
- Edit a student.
- Delete a student.
- Request a student ID that does not exist.
- Open the application on a mobile screen.

## Future Enhancements

- User login and authentication.
- Admin and student roles.
- Student profile photo upload.
- Attendance management.
- Course and subject management.
- Pagination.
- Export student records to CSV or PDF.
- MySQL or PostgreSQL database support.
- Dashboard with student statistics.
- Improved API authentication.

## Project Purpose

This project was created as a college-level full-stack web development project to demonstrate:

- CRUD operations.
- Flask routing.
- Database integration.
- HTML template rendering.
- Form validation.
- REST API development.
- Git and GitHub usage.
- Web application deployment.

## Author

Student Management System Project

Developed as an academic project.

## License

This project is intended for educational purposes.
