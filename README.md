# Student Management System

A simple web-based Student Management System built with Flask, SQLite, HTML, CSS, JavaScript, Bootstrap, and Jinja2.

The application allows an administrator to log in and add, view, search, update, and delete student records.

## Features

- Admin login and logout.
- Dashboard with student statistics.
- Add new student records.
- View all student records.
- Search students by name, email, department, or phone number.
- Edit existing student details.
- Delete student records.
- Validate required fields.
- Validate email addresses.
- Validate 10-digit phone numbers.
- Validate student year from 1 to 4.
- Prevent duplicate email addresses.
- Responsive Bootstrap user interface.
- SQLite database integration.
- REST API endpoints for student records.
- Production deployment with Gunicorn.

## Technology Stack

- Python 3
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
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
    ├── login.html
    ├── dashboard.html
    ├── students.html
    ├── index.html
    └── edit.html
```

## Database Structure

The application uses a SQLite database named `students.db`.

The `students` table contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique student ID |
| `name` | Student full name |
| `email` | Student email address |
| `phone` | Student phone number |
| `department` | Student department |
| `year` | Student academic year |
| `address` | Student address |
| `created_at` | Record creation date and time |

## Requirements

Install the following software:

- Python 3
- VS Code
- Git
- A web browser

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/Madhushree-tech26/Student-management-system.git](https://github.com/Madhushree-tech26/Student-management-system.git)
```

### 2. Open the project folder

```bash
cd Student-management-system
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

### 5. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Application Locally

Start the Flask application:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000/login
```

## Default Login

For the current demonstration version, use:

```text
Username: admin
Password: admin123
```

After logging in, you can open:

```text
http://127.0.0.1:5000/dashboard
```

```text
http://127.0.0.1:5000/students
```

> For a real production application, replace the hard-coded login with a database-based authentication system and hashed passwords.

## How to Use

### Log in

1. Open the login page.
2. Enter the username and password.
3. Click **Login**.

### Add a student

1. Open the student management page.
2. Enter the student's name.
3. Enter the student's email.
4. Enter a 10-digit phone number.
5. Select the department.
6. Select the academic year.
7. Enter the address.
8. Click **Add Student**.

### View students

All saved student records appear in the student records table.

### Search students

Enter a name, email, department, or phone number in the search box and click **Search**.

### Edit a student

1. Click the **Edit** button for a student.
2. Modify the student information.
3. Click **Save Changes**.

### Delete a student

1. Click the **Delete** button.
2. Confirm the deletion.

## Web Routes

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to login or dashboard |
| `GET`, `POST` | `/login` | Login page and login processing |
| `GET` | `/logout` | Logs out the current user |
| `GET` | `/dashboard` | Displays dashboard statistics |
| `GET` | `/students` | Displays and searches students |
| `POST` | `/add` | Adds a new student |
| `GET`, `POST` | `/edit/<id>` | Displays or updates a student |
| `POST` | `/delete/<id>` | Deletes a student |

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/students` | Get all students |
| `POST` | `/api/students` | Create a student |
| `GET` | `/api/students/<id>` | Get one student |
| `PUT` | `/api/students/<id>` | Update a student |
| `DELETE` | `/api/students/<id>` | Delete a student |

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

## Validation Rules

The application applies these validation rules:

- Student name cannot be empty.
- Email address is required.
- Email address must use a valid format.
- Phone number must contain exactly 10 digits.
- Department is required.
- Year must be between 1 and 4.
- Email addresses must be unique.
- Server-side validation is applied before saving data.

## Environment Variables

For deployment, configure the following environment variable:

```text
SECRET_KEY=your-long-random-secret-key
```

Do not commit real passwords, API keys, or secret keys to GitHub.

The application reads the secret key using:

```python
app.secret_key = os.environ.get("SECRET_KEY")
```

## Dependencies

The `requirements.txt` file contains:

```text
Flask==3.1.0
gunicorn==23.0.0
```

## Run with Gunicorn

For deployment, run:

```bash
gunicorn app:app
```

The `Procfile` contains:

```text
web: gunicorn app:app
```

## Deployment with Render

This project can be deployed using Render or another Python-compatible hosting service.

Use these Render settings:

```text
Build Command:
pip install -r requirements.txt
```

```text
Start Command:
gunicorn app:app
```

Add this environment variable in Render:

```text
Key: SECRET_KEY
Value: your-long-random-secret-key
```

After deployment, Render provides a public website URL.

> SQLite is suitable for local development and academic demonstrations. For a production application, use a persistent database such as PostgreSQL because local files may not persist on some cloud hosting services.

## Testing Checklist

Test the following operations:

- Log in with valid credentials.
- Try logging in with invalid credentials.
- Add a student with valid information.
- Submit the form with missing information.
- Enter an invalid email address.
- Enter an invalid phone number.
- Enter an invalid academic year.
- Add a duplicate email address.
- Search for a student.
- Edit a student.
- Delete a student.
- Request a student ID that does not exist.
- Open the application on a mobile screen.
- Test the REST API endpoints.

## Future Enhancements

- Database-based user authentication.
- Password hashing.
- Admin and student roles.
- Student profile photo upload.
- Attendance management.
- Course and subject management.
- Pagination.
- Export student records to CSV or PDF.
- MySQL or PostgreSQL database support.
- CSRF protection.
- API authentication.
- Improved dashboard charts.

## Project Purpose

This project was created as a college-level full-stack web development project to demonstrate:

- CRUD operations.
- Flask routing.
- SQLite database integration.
- HTML template rendering.
- Form validation.
- REST API development.
- User login and sessions.
- Responsive web design.
- Git and GitHub usage.
- Web application deployment.

## Author

Student Management System Project

Developed as an academic project.

## License

This project is intended for educational purposes.
