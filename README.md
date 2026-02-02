# 📝 Mini Task Manager
A simple Task Management application built using **Python**, **Flask**, **SQLAlchemy**, **Jinja2**, and **PostgreSQL**.


## 🚀 Features
- Create tasks
- View all tasks
- Update task details
- Delete tasks
- Toggle task status (Todo → In Progress → Done)
- Filter and search tasks
- REST API with consistent response format
- File-based logging


## 🛠 Tech Stack
- **Backend:** Flask (Python)
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Templating:** Jinja2
- **Logging:** Python logging


## 📂 Project Structure
```bash
mini-task-manager  
│──── static/  
│       └── style.css
├──── templates/  
│       └── index.html
│       └── tasks.html
├──── app.py
├──── .gitignore
├──── requirements.txt
└──── README.md  
```


### **1. Create Tasks**
- **Endpoint**: **`/api/tasks`**
- **Method:** `POST`
- **Sample Request Body**:

```json
{
    "title": "Complete project documentation",
    "description": "Write README, API docs, and finalize project notes",
    "status": "in_progress",
    "due_date": "2026-02-10"
}
```

- **Sample Response**:

```json
{
    "data": {
        "created_at": "2026-02-02T09:26:28.635734",
        "description": "Write README, API docs, and finalize project notes",
        "due_date": "2026-02-10",
        "id": 18,
        "status": "in_progress",
        "title": "Complete project documentation"
    },
    "status": 201,
    "success": "Task created successfully"
}
```

### **2. Get Tasks**
- **Endpoint**: **`/api/tasks`**
- **Method:** `GET`
- **Query Params:** `?status={todo status}&q={description | title}&sort={due_date | created_date}`
- **Sample Response**:

```json
{
    "data": [
        {
            "created_at": "2026-02-02T09:26:28.635734",
            "description": "Write README, API docs, and finalize project notes",
            "due_date": "2026-02-10",
            "id": 18,
            "status": "in_progress",
            "title": "Complete project documentation"
        },
        ...
    ],
    "status": 200,
    "success": "Tasks fetched successfully"
}
```

### **3. Update Task**
- **Endpoint**: **`/api/tasks/:id`**
- **Method:** `PUT`
- **Sample Request Body**:

```json
{
    "title": "Complete project documentation - Flask",
    "status": "done",
}
```

- **Sample Response**:

```json
{
    "data": {
        "created_at": "2026-02-02T09:26:28.635734",
        "description": "Write README, API docs, and finalize project notes",
        "due_date": "2026-02-10",
        "id": 18,
        "status": "done",
        "title": "Complete project documentation - Flask"
    },
    "status": 200,
    "success": "Task updated successfully"
}
```


### **4. Get Single Task**
- **Endpoint**: **`/api/tasks/:id`**
- **Method:** `GET`
- **Sample Response**:

```json
{
    "data": {
        "created_at": "2026-02-02T09:26:28.635734",
        "description": "Write README, API docs, and finalize project notes",
        "due_date": "2026-02-10",
        "id": 18,
        "status": "done",
        "title": "Complete project documentation - Flask"
    },
    "status": 200,
    "success": "Task fetched successfully"
}
```

### **5. Delete Task**
- **Endpoint**: **`/api/tasks/:id`**
- **Method:** `DELETE`
- **Sample Response**:

```json
{
    "status": 200,
    "success": "Task deleted successfully"
}
```

### **6. Cycleic Toggle Task Status (Todo -> In Progress -> Done)**
- **Endpoint**: **`/api/tasks/:id/toggle`**
- **Method:** `POST`
- **Sample Response**:

```json
{
    "status": "todo",
    "status-code": 200,
    "success": "Toggle status successfully"
}
```

### **7. Some Error Response**
```json
{
    "error": "Title is not found",
    "status": 404
}
```
```json
{
    "error": "Status must be 'todo', 'in_progress', 'done'",
    "status": 400
}
```
```json
{
    "error": "Task not found for id: 100",
    "status": 404
}
```


## Getting Started
Follow these steps to set up and run the project locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/Jakaria030/mini-task-manager.git
    ```
2. Navigate to the project directory:
    ```bash
    cd mini-task-manager
    ```
3. Create Virtual Environment
    ```bash
    python3 -m venv .venv # for linux
        
    python -m venv .venv # for windows
    ```
4. Activate Virtual Environment
    ```bash
    source .vevn/bin/activate # for linux
    vevn\Scripts\activate # for windows
    ```
5. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
6. Save Intsalled Packages
    ```bash
    pip freeze > requirements.txt
    ```
7. Run PostgreSQL container
    ```bash
    docker run -d --name task-manager-db -e POSTGRES_DB=tasksdb -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v pgdata:/var/lib/postgresql/data postgres
    ```
8. Connect PostgreSQL via docker
    ```bash
    docker exec -it task-manager-db psql -U postgres -d tasksdb
    ```
9. Run the development server:
    ```bash
    python app.py
    ```

**NOTE:** 7 and 8 commands run another terminal or you can setup Postgresql database another way. In that case you have to replace conection string on app.py

## Additional Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [Jinja Documentation](https://jinja.palletsprojects.com/en/stable/)

