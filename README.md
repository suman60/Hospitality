# 🏨 Hospitality Analytics Platform

A lightweight **FastAPI-based backend service** for the hospitality industry (hotels, resorts, restaurants) that centralizes operational and sales transaction data with analytics.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Data Model](#-data-model)
- [API Endpoints](#-api-endpoints)
- [Authentication](#-authentication)
- [Setup & Installation](#-setup--installation)
- [Running with Docker](#-running-with-docker)

---

## 📌 Project Overview

This service allows to:

- ✅ Store incoming transaction data via API
- ✅ Bulk upload transaction data via JSON or CSV file
- ✅ Retrieve and filter transaction records
- ✅ Generate business analytics (total sales, top properties)
- ✅ Secure write operations with JWT authentication
- ✅ Run entirely inside a Docker container

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10** | Core language |
| **FastAPI** | Web framework & API routing |
| **SQLAlchemy** | ORM for database operations |
| **SQLite** | Lightweight embedded database |
| **Pydantic** | Request/response validation |
| **passlib + bcrypt** | Password hashing |
| **Docker** | Containerization |

---

## 📁 Project Structure

```
hospitality-analytics/
│
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app, router registration, DB init
│   ├── database.py       # SQLAlchemy engine, session, Base
│   ├── models.py         # ORM models (Transaction, User)
│   ├── schemas.py        # Pydantic schemas (input/output validation)
│   ├── crud.py           # Database operations
│   ├── auth.py           # JWT creation, verification, password hashing
│   └── routers/
│       ├── __init__.py
│       ├── transactions.py   # Transaction CRUD endpoints
│       ├── analytics.py      # Analytics endpoints
│       └── auth.py           # Register & Login endpoints
│
├── Dockerfile
├── requirements.txt
├── sample_data.csv
└── README.md
```

---

## 🗄 Data Model

### Transaction Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique transaction ID |
| `property_name` | String | NOT NULL, Indexed | Hotel or restaurant name |
| `category` | String | NOT NULL | room_booking / food / service / spa |
| `price` | Float | NOT NULL, > 0 | Price per unit |
| `quantity` | Integer | NOT NULL, >= 1 | Number of units |
| `date` | Date | NOT NULL | Format: YYYY-MM-DD |
| `created_at` | DateTime | Auto-set on insert | Record creation timestamp |

### User Table

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key, Auto-increment | Unique user ID |
| `username` | String | Unique, NOT NULL | Login username |
| `hashed_password` | String | NOT NULL | bcrypt hashed password |

---

## 🔌 API Endpoints

### Transactions

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/transactions/` | ✅ Yes | Add a single transaction |
| `POST` | `/transactions/bulk` | ❌ No | Add multiple transactions (JSON array) |
| `POST` | `/transactions/upload-csv` | ❌ No | Upload a CSV file of transactions |
| `GET` | `/transactions/` | ❌ No | List transactions with optional filters |

#### GET /transactions — Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `category` | string | No | Filter by category (e.g. `food`) |
| `start_date` | date | No | Filter from this date (YYYY-MM-DD) |
| `end_date` | date | No | Filter up to this date (YYYY-MM-DD) |

### Analytics

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/analytics/total-sales` | ❌ No | Total revenue and transaction count |
| `GET` | `/analytics/top-properties` | ❌ No | Top 3 properties by revenue |

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive a JWT token |

---

## 🔐 Authentication

This project uses **JWT (JSON Web Token)** Bearer authentication.

### How it works

1. Register a user via `POST /auth/register`
2. Login via `POST /auth/login` — receive an `access_token`
3. Include the token in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_access_token>
```

### Token Details

| Property | Value |
|---|---|
| Algorithm | HS256 |
| Expiry | 30 minutes |
| Header | `Authorization: Bearer <token>` |

### Which endpoints require auth?

| Endpoint | Protected |
|---|---|
| POST /transactions | ✅ Yes |
| POST /transactions/bulk | ❌ No |
| POST /transactions/upload-csv | ❌ No |
| GET /transactions | ❌ No |
| GET /analytics/* | ❌ No |
| POST /auth/register | ❌ No |
| POST /auth/login | ❌ No |

---

## ⚙️ Setup & Installation

### Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

---

## 🐳 Running with Docker

> **Recommended method** — no local Python setup needed.

### Step 1 — Clone the repository

```bash
git clone https://github.com/suman60/Hospitality.git
```

### Step 2 — Build the Docker image

```bash
docker build -t fastapi-app .
```

> If you face timeout errors due to slow internet, use:
> ```bash
> docker build --no-cache -t fastapi-app .
> ```

### Step 3 — Run the container

```bash
docker run -p 8000:8000 fastapi-app
```

### Step 4 — Open in browser

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | ✅ Swagger UI (interactive API docs) |

> ⚠️ **Do NOT use** `http://0.0.0.0:8000` in your browser — use `localhost` instead.
---

