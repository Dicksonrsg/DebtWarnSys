run:
	@python manage.py runserver

create-app:
	@source setenv.sh &&\
	python manage.py startapp website

create-migration:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

create-super:
	python manage.py createsuperuser

format:
	@poetry run python -m black webpage && \
	poetry run python -m isort --atomic webpage && \
	poetry run python -m autoflake --remove-all-unused-imports --remove-unused-variables --recursive --in-place webpage
