# cyber-students-secure-api

This project is part of the **Modern Cryptography and Security Management & Compliance** assignment. It is based on the provided starter code and has been extended to implement secure handling of user data.

## Security Enhancements Implemented

I improved the original system by adding the following security features:

* Password hashing using salt and multiple iterations
* Token-based authentication with expiration
* Token hashing before storage
* Encryption of sensitive personal data:

  * Full name
  * Phone number
  * Address
  * Date of birth
  * Disability information
* Secure logout functionality (token invalidation)

These changes ensure that even if the database is accessed, sensitive data is not readable.

---

## Setup the Project

### 1. Create a virtual environment

```bash
python -m venv project-venv
```

### 2. Activate the environment

```bash
source project-venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

Start MongoDB and run:

```bash
mongosh
```

Then create the database:

```bash
use cyberStudents;
db.createCollection('users');
```

---

## Run the Server

```bash
python run_server.py
```

The server runs at:

http://localhost:4000/students/api

---

## API Endpoints

### Register User

```bash
curl -X POST http://localhost:4000/students/api/registration -d '{
  "email": "user@example.com",
  "password": "secure123",
  "displayName": "User",
  "fullName": "John Doe",
  "phone": "123456789",
  "address": "Street 1",
  "dob": "2000-01-01",
  "disability": "None"
}'
```

---

### Login

```bash
curl -X POST http://localhost:4000/students/api/login -d '{
  "email": "user@example.com",
  "password": "secure123"
}'
```

Response:

```json
{
  "token": "generated_token",
  "expiresIn": 1234567890
}
```

---

### Get User Profile

```bash
curl -H "X-Token: YOUR_TOKEN" http://localhost:4000/students/api/user
```

---

### Logout

```bash
curl -X POST -H "X-Token: YOUR_TOKEN" http://localhost:4000/students/api/logout
```

---

## Run Tests

```bash
python run_test.py
```

All tests should pass successfully.

---

## Hacker Script (Security Demonstration)

Run:

```bash
python run_hacker.py list
```

Before the security implementation:

* Passwords were stored in plain text
* Personal data was readable

After the implementation:

* Passwords are hashed
* Tokens are hashed
* Personal data is encrypted (stored as ciphertext with nonce)

This demonstrates improved protection against data breaches.

---

## Project Structure

```
api/
  handlers/
    registration.py
    login.py
    logout.py
    user.py
  security_utils.py

test/
run_server.py
run_test.py
run_hacker.py
```

---

## Acknowledgement

This project is based on the starter code and guidance provided as part of the **Modern Cryptography and Security Management & Compliance** course. I extended the original implementation by adding security features such as password hashing, token security, and data encryption.

---

## Author

Developed by:

Bello

---

## Summary

This project demonstrates:

* Secure password handling
* Token-based authentication
* Data encryption techniques
* Protection against common security vulnerabilities
