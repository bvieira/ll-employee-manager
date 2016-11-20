# ll-employee-manager

## build
docker-compose build
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

## run
docker-compose up

## django admin
### create user
docker-compose run web python manage.py createsuperuser