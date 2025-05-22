# 🚀 Flask + MySQL Two-Tier Dockerized Application

A simple yet powerful two-tier web application using **Flask** for the backend and **MySQL** as the database. Both services are containerized using **Docker** and connected through a custom **Docker network**, demonstrating real-world DevOps practices for service isolation, networking, and persistent data management.

---

## 🧰 Technologies Used

- 🐍 Python (Flask)
- 🐬 MySQL 8.0
- 🐳 Docker & Docker Compose
- 📦 Docker Volumes for persistence
- 🔄 Docker Networking

---

## 📁 Project Structure

```
flask_two_tier_docker/
├── app/
│   ├── app.py               # Flask application
│   └── requirements.txt     # Python dependencies
│
├── Dockerfile               # Docker build config for Flask
├── docker-compose.yml       # Defines and connects Flask + MySQL services
└── README.md                # Project documentation
```

---

## 🔧 Prerequisites

Before running this project, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚀 Getting Started

### Step-by-Step Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/Alok77it/flask_two_tier_docker.git
cd flask_two_tier_docker
```

#### 2. Build and Run with Docker Compose

```bash
docker-compose up --build
```

#### 3. Access the Flask App

Open your browser and go to:

```
http://localhost:5000
```

You should see a response similar to:

```
Database time: 2025-05-22 13:45:00
```

---

## ⚙️ How It Works

- The `flask_app` service is built from the Dockerfile, installs Python requirements, and starts the Flask server.
- The `mysql_db` service uses the official MySQL image, with environment variables to initialize the database and password.
- Docker creates a custom bridge network `app_net` so both services can communicate internally.
- Flask connects to MySQL using the internal hostname `mysql_db`.

---

## 🐳 Docker Compose Overview

```yaml
version: "3.8"

services:
  flask_app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mysql_db
    networks:
      - app_net

  mysql_db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: flask_db
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app_net

volumes:
  mysql_data:

networks:
  app_net:
```

---

## 📦 Dockerfile (Flask App)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ .

CMD ["python", "app.py"]
```

---

## 💾 Persistent Storage

All MySQL data is stored in a named volume called `mysql_data`.

This ensures your data persists even if you stop or rebuild containers.

---

## 📄 Flask App Example (`app/app.py`)

```python
from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    connection = mysql.connector.connect(
        host='mysql_db',
        user='root',
        password='rootpassword',
        database='flask_db'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return f"Database time: {result[0]}"
```

---

## ✅ Future Improvements

- 🔐 Use `.env` for managing secrets securely
- 🔁 Add retry logic in Flask for MySQL connection during startup
- 🔍 Add a health check endpoint for container monitoring
- ⚙️ CI/CD pipeline integration (GitHub Actions, Jenkins, etc.)

---

## 📜 License

MIT License – you're free to use and modify this project as needed.

---

## 🙌 Author

Made with ❤️ by Alok Trivedi

If you found this project useful, feel free to ⭐ the repository and share feedback or suggestions via Issues.
