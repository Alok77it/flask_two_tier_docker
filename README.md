# 🚀 Flask + MySQL Two-Tier Application using Docker (Without Compose)

A lightweight two-tier web application that uses **Flask** (Python) for frontend/backend logic and **MySQL** as the database. Both run in Docker containers, networked via a custom Docker network—**no `docker-compose` needed!**

---

## 📸 Features

- 🧾 User form to submit **Name** and **Date of Birth**
- 💾 Automatically creates a `users` table in MySQL if it doesn't exist
- 🔁 Data insertion and retrieval using Python's `mysql-connector-python`
- 🌐 Separate page (`/users`) to list all submitted users
- 🐳 Fully containerized with custom Docker networking

---

## 🗂️ Project Structure

```
flask_two_tier_docker/
├── app/
│   ├── app.py               # Flask app with HTML form + DB logic
│   └── requirements.txt     # Python dependencies
├── Dockerfile               # Flask Docker build file
└── README.md                # Project documentation (this file)
```

---

## 🧠 How It Works

1. **Two containers** are run manually:
    - One for the **Flask app**
    - One for **MySQL DB**
2. Both attach to the same custom Docker network (`app_net`).
3. The Flask app:
    - Connects to MySQL via container name `mysql_db`
    - Auto-creates `users` table if missing
    - Accepts form data (`name`, `dob`) via POST
    - Inserts data into MySQL
    - `/users` route lists all users

---

## 🛠️ Prerequisites

- Docker installed and running
- No need for Docker Compose or extra tools

---

## ⚙️ Setup & Run (Step-by-Step)

> **Run these commands from your project root**

### 🧱 1. Build Flask Image

```bash
docker build -t flask-app .
```

### 🌐 2. Create Custom Docker Network

```bash
docker network create app_net
```

### 🐬 3. Run MySQL Container

```bash
docker run -d \
  --name mysql_db \
  --network app_net \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=flask_db \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0
```

### 🔥 4. Run Flask Container

```bash
docker run -d \
  --name flask_app \
  --network app_net \
  -p 5000:5000 \
  flask-app
```

---

### 🌐 Access the Application

- **Form:** [http://localhost:5000](http://localhost:5000)
- **User List:** [http://localhost:5000/users](http://localhost:5000/users)

---

## 🧪 Example

### 👤 Add a User

- Name: `Alice`
- DOB: `1995-07-14`
- Submit the form → redirected to `/users`

### 📋 View Users

| ID | Name  | Date of Birth |
|----|-------|---------------|
| 1  | Alice | 1995-07-14    |

---

## 🧹 Cleanup

```bash
docker stop flask_app mysql_db
docker rm flask_app mysql_db
docker volume rm mysql_data
docker network rm app_net
```

---

## 📦 Dependencies

- Python 3.9
- Flask
- mysql-connector-python
- MySQL 8.0 Docker Image

---

## 📌 Notes

- The MySQL host inside the Flask app must be set to `mysql_db` (the container name), **not** `localhost`.
- Table is auto-created on the first request if it doesn't exist.

---

## 📈 Future Enhancements

- ✅ Validation and error handling
- 🔐 Login/auth system
- 📜 Pagination of users
- 📊 Export to CSV or Excel
- 🌍 Deploy to cloud (AWS/GCP)

---

## 🤝 Author

**Alok Trivedi**  
[GitHub](https://github.com/Alok77it) | [LinkedIn](https://www.linkedin.com/in/aloktrivedi/)

---

## 🏁 License

This project is licensed under the MIT License.
---
