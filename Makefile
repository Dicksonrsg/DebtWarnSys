install:
	@poetry install

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

test:
	export DJANGO_ENV=test && poetry run pytest --ds=dws.settings

coverage:
	@export DJANGO_ENV=test && \
	echo "Generating html report" && \
	pytest --cov-report html --cov=./