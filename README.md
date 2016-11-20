# ll-employee-manager

## build
### build docker images
docker-compose build
### execute migrations
docker-compose run web python manage.py migrate
### create user
docker-compose run web python manage.py createsuperuser

## run
docker-compose up

## api

## admin