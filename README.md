# Social Media Backend API

A production-style social media backend built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

This project implements core social media functionality including user authentication, posts, likes, comments, following users, saved posts, automated testing, Docker support, and CI/CD with GitHub Actions.

---

## Features

### Authentication
- User Registration
- User Login
- JWT Access Tokens
- Protected Routes
- Password Hashing using bcrypt

### Users
- Create Account
- Get User Profile
- Update User Profile
- Delete User Account
- Follower Count
- Following Count

### Posts
- Create Posts
- Read Posts
- Update Posts
- Delete Posts
- Pagination
- Search Posts

### Likes / Votes
- Like Posts
- Remove Likes
- Prevent Duplicate Likes

### Comments
- Add Comments
- View Comments
- Delete Comments

### Follow System
- Follow Users
- Unfollow Users
- Prevent Self Follow
- Prevent Duplicate Follows

### Saved Posts
- Save Posts
- Unsave Posts
- View Saved Posts

### Database
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Optimized Database Indexes

### Testing
- Pytest
- Dedicated Test Database
- 54 Automated Tests

### DevOps
- Docker
- Docker Compose
- GitHub Actions CI/CD

---

## Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| Password Hashing | bcrypt |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

## Project Structure

```text
app/
│
├── routers/
│   ├── auth.py
│   ├── user.py
│   ├── post.py
│   ├── vote.py
│   ├── comments.py
│   ├── follow.py
│   └── saved_posts.py
│
├── models.py
├── schemas.py
├── database.py
├── oauth2.py
├── utils.py
├── config.py
└── main.py

tests/
│
├── conftest.py
├── test_auth.py
├── test_users.py
├── test_posts.py
├── test_comments.py
├── test_follow.py
└── test_saved_posts.py

alembic/
docker-compose-dev.yml
Dockerfile
requirements.txt
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | /login | Login user |

### Users

| Method | Endpoint |
|----------|----------|
| POST | /users |
| GET | /users |
| GET | /users/{id} |
| PUT | /users/{id} |
| DELETE | /users/{id} |

### Posts

| Method | Endpoint |
|----------|----------|
| POST | /sqlalchemy |
| GET | /sqlalchemy |
| GET | /sqlalchemy/{id} |
| PUT | /sqlalchemy/{id} |
| DELETE | /sqlalchemy/{id} |

### Votes

| Method | Endpoint |
|----------|----------|
| POST | /vote |

### Comments

| Method | Endpoint |
|----------|----------|
| POST | /comments/{post_id} |
| GET | /comments/{post_id} |
| DELETE | /comments/{id} |

### Follow

| Method | Endpoint |
|----------|----------|
| POST | /follow |
| DELETE | /follow/{user_id} |

### Saved Posts

| Method | Endpoint |
|----------|----------|
| POST | /saved/{post_id} |
| DELETE | /saved/{post_id} |
| GET | /saved |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=yourpassword

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Migration

```bash
alembic upgrade head
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## Running Tests

```bash
pytest
```

Current Test Coverage:

```text
54 Tests Passing
```

---

## Docker

Build Image

```bash
docker build -t social-media-api .
```

Run Container

```bash
docker run -p 8000:8000 social-media-api
```

Using Docker Compose

```bash
docker-compose -f docker-compose-dev.yml up
```

---

## CI/CD

GitHub Actions automatically:

- Installs dependencies
- Creates PostgreSQL service
- Runs all tests
- Verifies build health on every push and pull request

## Author

Prajwal Vasista

Computer Science Engineering Student

Built to learn backend development, testing, Docker, and CI/CD using FastAPI.