# Task Manager API with Telegram Bot Integration

**Django REST Framework** project for managing tasks with **JWT authentication**, **Telegram notifications**, and **filtering/search functionality**.

## Features
- **User authentication** with JWT (`djangorestframework-simplejwt`)
- **Task management API** (CRUD operations)
- **Comment system** for tasks
- **Filtering & Searching** (by status, priority)
- **Telegram bot integration** for task notifications
- **PostgreSQL** (or SQLite for development)

## Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

### 2️⃣ Create & Activate Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the project root and add:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=sqlite:///db.sqlite3  # Change this for PostgreSQL if required
```

### 5️⃣ Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Run the Server
```sh
python manage.py runserver
```
API will be available at **`http://127.0.0.1:8000/api/`**.

---

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

## License
This project is licensed under the **MIT License**.

## Author

**Valeriy Abramov**
- GitHub:
- email: valery.abramov12@gmail.com