---

# Codeleap API

This project is a Django REST Framework (DRF) application implementing the Codeleap API. It allows users to create posts, add comments, like/unlike posts, and optionally include images in posts. It also includes automated testing and CI setup for GitHub Actions.

---

## Table of Contents

* [Installation](#installation)
* [Running the Project](#running-the-project)
* [API Documentation](#api-documentation)
* [Testing](#testing)
* [Insomnia Collection](#insomnia-collection)
* [Continuous Integration (CI)](#continuous-integration-ci)

---

## Project Structure

---

## Installation

1. Clone the repository:

```
git clone <repository_url>
cd codeleap
```

2. Create a Python virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root (or `codeleap/` folder) with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://myuser:mypassword@db:5432/mydatabase
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Running the Project

### Using Docker

1. Build and start the containers:

```
docker compose up --build
```

2. The web server will be available at `http://localhost:8000/`.

### Without Docker (Local SQLite for testing)

1. Run migrations:

```
python manage.py migrate
```

2. Start the development server:

```
python manage.py runserver
```

---

## API Documentation

Swagger documentation is available at:

```
http://localhost:8000/swagger/
```

It provides detailed information on all endpoints, parameters, and request/response structures.

---

## Testing

Automated tests are included using `pytest` and Django REST Framework test client.

1. Install `pytest` and `pytest-django` if not already installed:

```
pip install pytest pytest-django
```

2. Run the tests:

```
pytest api/tests.py
```

All tests will run against the local SQLite database by default for CI purposes.

---

## Insomnia Collection

You can import the provided `codeleap_insomnia.json` into **Insomnia** to quickly test all API endpoints.

* Ensure `Content-Type: application/json` is set for POST requests (especially for creating posts and comments).
* Use the query parameters for filtering posts by username.
* Like/Unlike endpoints are available under `/careers/{id}/like/` and `/careers/{id}/unlike/`.

---

## Continuous Integration (CI)

GitHub Actions are configured to run automated tests on push or pull request:

* Workflow uses Python 3.13.
* Runs `pytest` using an in-memory SQLite database to avoid dependency on Docker or PostgreSQL.
* No migrations or external database required for CI; the CI is self-contained.

You can view the workflow configuration in `.github/workflows/ci.yml`.

---

## Notes

* The `Post` model supports optional images for posts.
* Posts can have multiple comments; the API handles comments creation per post.
* The `username` field is mandatory for both posts and comments.
* Likes are handled as a counter on the post.

---
