ll-employee-manager
======================

# Build
build docker images and start up database
```sh
$ docker-compose up --build
```
stop the service and execute migrations
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
- [Get Employee](#get-employee)

## List Employees
returns a list of exisisting employees

### Request:
`GET` /employee

### Response:
- list of [Employee Response](#employee-response)

	```sh
	$ curl -v "localhost:8000/employee/"
	> GET /employee/ HTTP/1.1
	> Host: localhost:8000
	> User-Agent: curl/7.43.0
	> Accept: */*
	>
	< HTTP/1.0 200 OK
	< Date: Sun, 20 Nov 2016 15:11:16 GMT
	< Server: WSGIServer/0.2 CPython/3.5.2
	< X-Frame-Options: SAMEORIGIN
	< Content-Type: application/json
	<
	[{"department": "Tecnologia", "email": "user1@email.com", "name": "user1", "id": 1}, {"department": "Tecnologia", "email": "user2@email.com", "name": "user2", "id": 2}]
	
	```

## Get Employee
returns employee by id

### Request:
`GET` /employee/:id


| param   | description           |
|-------------------|-----------------------|
| `:id`             | `id` from employee  |

### Response:
- [Employee Response](#employee-response)

	```sh
	$ curl -v "localhost:8000/employee/1/"
	> GET /employee/1/ HTTP/1.1
	> Host: localhost:8000
	> User-Agent: curl/7.43.0
	> Accept: */*
	>
	< HTTP/1.0 200 OK
	< Date: Sun, 20 Nov 2016 15:21:07 GMT
	< Server: WSGIServer/0.2 CPython/3.5.2
	< X-Frame-Options: SAMEORIGIN
	< Content-Type: application/json
	<
	{"department": "Tecnologia", "email": "user1@email.com", "name": "user1", "id": 1}
	
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
