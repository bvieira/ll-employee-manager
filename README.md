ll-employee-manager
======================

# Build
build docker images
```sh
$ docker-compose build
```
execute migrations
```sh
$ docker-compose run web python manage.py migrate
```

# Create user
```sh
$ docker-compose run web python manage.py createsuperuser
```

# Run
```sh
$ docker-compose up
```

# API
- [List Employees](#list-employee)

## List Employees
returns a list of exisisting employees

### Request:
`GET` /employee

### Response:
- list of [Employee Response](#employee-response)

	```sh
	$ curl -v "localhost:8000/employee/"
	```

# Schema
## Employee Request

	{
		"name": string,
		"email": string,
		"department": string
	}

## Employee Response

	{
		"id": integer,
		"name": string,
		"email": string,
		"department": string
	}

# Admin
Admin is provided by django, and can be accessed on path '/admin', if user/password was not created yet, [create user now](#create-user)

eg.
```sh
localhost:8000/admin/
```
