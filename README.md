# Task Manager API (Django + Telegram Bot Integration)

## Overview
A task tracking API built with Django REST Framework, featuring JWT authentication, comment support, search & filtering, and real-time notifications via Telegram Bot. Ideal for managing personal or team to-dos with programmatic access.

## Features
- **User authentication** with JWT (`djangorestframework-simplejwt`)
- **Task management API** (CRUD operations)
- **Comment system** for tasks
- **Filtering & Searching** (by status, priority)
- **Telegram bot integration** for task notifications
- **PostgreSQL** (or SQLite for development)

## Installation

1. Clone the Repository
```sh
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

2. Create & Activate Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install Dependencies
```sh
pip install -r requirements.txt
```

4. Set Up Environment Variables
Create a `.env` file in the project root and add:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=sqlite:///db.sqlite3
```

5. Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

6. Run the Server
```sh
python manage.py runserver
```
API will be available at **`http://127.0.0.1:8000/api/`**.


## Technologies Used:
- **Python 3.10+**
- **Django 4+**
- **Django REST Framework**
- **PostgreSQL** or SQLite
- **Telegram Bot API**
- **JWT (djangorestframework-simplejwt)**


## API Endpoints
### **Authentication**
| Method | Endpoint               | Description                |
|--------|------------------------|----------------------------|
| POST   | `/api/auth/token/`      | Obtain JWT access token   |
| POST   | `/api/auth/token/refresh/` | Refresh JWT token  |

### **Task Management**
| Method | Endpoint         | Description                 |
|--------|----------------|-----------------------------|
| GET    | `/api/tasks/`  | List all tasks              |
| POST   | `/api/tasks/`  | Create a new task           |
| GET    | `/api/tasks/{id}/` | Retrieve a specific task  |
| PUT    | `/api/tasks/{id}/` | Update a task            |
| DELETE | `/api/tasks/{id}/` | Delete a task            |

### **Comments**
| Method | Endpoint                          | Description                 |
|--------|-----------------------------------|-----------------------------|
| GET    | `/api/tasks/{task_id}/comments/` | List comments for a task    |
| POST   | `/api/tasks/{task_id}/comments/` | Add a comment to a task     |

---

## Telegram Bot Integration
### Run the Telegram Bot:
```sh
python tasks/telegram_bot.py
```

### Available Commands:
- `/start` → Register and link Telegram
- `/tasks` → View tasks
- `/newtask <task>` → Create a task
- `/deletetask <task_id>` → Delete a task
- `/updatetask <task_id> <status>` → Update task status

---

## Author
**Valeriy Abramov**

- GitHub: [@abramov-v](https://github.com/abramov-v) 
- email: abramov.valeriy@hotmail.com
