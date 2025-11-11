# Древовидное меню

**Базу данных я специально не добавил в .gitignore чтобы были готовые данные для теста**

## Запуск
```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ - там пример с тремя меню

Админка: `/admin/`
