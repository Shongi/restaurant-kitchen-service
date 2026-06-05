# Restaurant Kitchen Service

A Django app for managing a restaurant kitchen: cooks, dishes, dish types, and ingredients.

## Setup

```bash
git clone <repo-url>
cd restaurant-kitchen-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tests

```bash
python manage.py test
```

## Features

- CRUD for Cooks, Dishes, Dish Types, Ingredients
- Search by name/username on list pages
- Pagination
- Toggle cook assignment to dishes
