# cyber-students-secure-api

This repository provides a secure REST API implementation for the Shared Project for Modern Cryptography and Security Management & Compliance.

This project builds upon the original sample code by improving security through password hashing, token-based authentication, and better data handling practices.

---

##  Remarks

This project is based on the original coursework provided by my lecturer for the Modern Cryptography and Security Management & Compliance module.

The base structure and initial implementation were provided as part of the academic project.
Enhancements, security improvements, and additional functionality were implemented by me.

---

##  Features

* User Registration
* User Login (Token-based authentication)
* Logout functionality
* User Profile retrieval
* Password hashing (secure storage)
* MongoDB database integration

---

##  Requirements

* Python 3
* MongoDB
* Git
* curl

---

##  Get the Code

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/cyber-students-secure-api.git
cd cyber-students-secure-api
```

---

##  Setup the Project

Create a virtual environment:

```sh
python -m venv project-venv
```

Activate it:

```sh
# macOS/Linux
source project-venv/bin/activate

# Windows
.\project-venv\Scripts\activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

---

##  Database Setup

Start MongoDB and open shell:

```sh
mongosh
```

Create database and collection:

```js
use cyberStudents;
db.createCollection('users');
```

---

##  Run the Server

```sh
python run_server.py
```

Server runs at:

```
http://localhost:4000/students/api
```

---

##  API Usage

### Register

```sh
curl -X POST http://localhost:4000/students/api/registration \
-d "{\"email\": \"test@example.com\", \"password\": \"pass123\", \"displayName\": \"Test User\"}"
```

---

### Login

```sh
curl -X POST http://localhost:4000/students/api/login \
-d "{\"email\": \"test@example.com\", \"password\": \"pass123\"}"
```

Response:

```json
{
  "token": "your_token_here",
  "expiresIn": 1234567890
}
```

---

### Get Profile

```sh
curl -H "X-Token: your_token_here" \
http://localhost:4000/students/api/user
```

---

### Logout

```sh
curl -X POST -H "X-Token: your_token_here" \
http://localhost:4000/students/api/logout
```

---

##  Run Tests

```sh
python run_test.py
```

---

##  Security Improvements

The original implementation stored passwords in plaintext.
This version improves security by:

* Hashing passwords before storing them
* Preventing duplicate user registration
* Using token-based authentication with expiration
* Reducing risk of credential exposure

---

##  Hacker Script

```sh
python run_hacker.py list
```

This script demonstrates what an attacker could see if the database is compromised.

 In this improved version, passwords are no longer stored in plaintext, making attacks significantly less effective.

---

##  Notes

* Tokens expire after a set time or logout
* MongoDB must be running locally
* Tests use an in-memory database (no MongoDB required)

---

##  Future Improvements

* Environment variables for secrets
* Docker support
* HTTPS deployment
* Rate limiting and API protection

---
