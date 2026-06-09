Перед первым запуском приложения выполните команду:
PYTHONPATH=. poetry run python scripts/reset_super_admin_password.py
PYTHONPATH=. poetry run python app/scripts/create_super_admin.py
poetry run uvicorn app.main:app --reload
rm -f *.db