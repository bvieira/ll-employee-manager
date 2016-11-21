ll-employee-manager
======================

# Build and run
Build docker images and start up
```sh
$ docker-compose up --build -d
```
Execute migrations
```sh
$ docker-compose run web python manage.py migrate
```
Create admin user
```sh
$ docker-compose run web python manage.py createsuperuser
```

# Stop
```sh
$ docker-compose stop
```

# Logs
```sh
$ docker-compose logs -f
```

# Admin
Admin is provided by django, and can be accessed on path '/admin', to login use user/password creating during the [Build and run](#build-and-run)

On admin you will be able to create/view/edit users (to access the API), employees and departments.

Access:
```sh
localhost:8000/admin/
```

# Tests
Run test
```sh
$ docker-compose run web python manage.py test
```
Create coverage report
```sh
docker-compose run web coverage run manage.py test
```

Report results
```sh
docker-compose run web coverage report -m
```

# API
- [List Employees](#list-employee)
- [Get Employee](#get-employee)
- [Create Employee](#create-employee)
- [Update Employee](#update-employee)
- [Remove Employee](#remove-employee)

## List Employees
returns a list of exisisting employees

### Request:
`GET` /employee/

### Response:
- list of [Employee Response](#employee-response)

### Response Codes:
| code   | description           |
|-------------------|-----------------------|
| 200             | success  |

### Example:
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
`GET` /employee/:id/


| param   | description           |
|-------------------|-----------------------|
| `:id`             | `id` from employee  |

### Response:
- [Employee Response](#employee-response)

### Response Codes:
| code   | description           |
|-------------------|-----------------------|
| 200             | success  |
| 404             | id not found  |
| 400             | id is invalid |

### Example:
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

## Create Employee
create a new employee and returns it

* uses basic auth, create user on [admin](#admin)

### Request:
`POST` /employee/

#### Body:
- [Employee Request](#employee-request)

### Response:
- [Employee Response](#employee-response)

### Response Codes:
| code   | description           |
|-------------------|-----------------------|
| 201             | created with success  |
| 400             | employee content is invalid |

### Example:
```sh
$ curl -v -X POST "localhost:8000/employee/" -d '{"department": "Tecnologia", "email": "user1@email.com", "name": "user1"}' -u user:userp123 -H "Content-Type: application/json"
> POST /employee/ HTTP/1.1
> Host: localhost:8000
> Authorization: Basic dXNlcjp1c2VycDEyMw==
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 73
>
< HTTP/1.0 201 Created
< Date: Sun, 20 Nov 2016 20:12:38 GMT
< Server: WSGIServer/0.2 CPython/3.5.2
< Content-Type: application/json
< X-Frame-Options: SAMEORIGIN
<
{"department": "Tecnologia", "email": "user1@email.com", "id": 1, "name": "user1"}

```

## Update Employee
update an employee by id

* uses basic auth, create user on [admin](#admin)


### Request:
`PUT` /employee/:id/

| param   | description           |
|-------------------|-----------------------|
| `:id`             | `id` from employee  |

#### Body:
- [Employee Request](#employee-request)


### Response:
- [Employee Response](#employee-response)

### Response Codes:
| code   | description           |
|-------------------|-----------------------|
| 202             | updated with success  |
| 404             | id not found  |
| 400             | id or employee content is invalid |

### Example:
```sh
$ curl -v -X PUT "localhost:8000/employee/1/" -d '{"department": "Arquitetura", "email": "user1@email.com", "name": "user1"}' -u user:userp123 -H "Content-Type: application/json"
> PUT /employee/1/ HTTP/1.1
> Host: localhost:8000
> Authorization: Basic dXNlcjp1c2VycDEyMw==
> User-Agent: curl/7.43.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 74
>
< HTTP/1.0 202 Accepted
< Date: Sun, 20 Nov 2016 21:34:28 GMT
< Server: WSGIServer/0.2 CPython/3.5.2
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
<
{"id": 1, "name": "user1", "email": "user1@email.com", "department": "Arquitetura"}

```

## Remove Employee
remove an employee by id

* uses basic auth, create user on [admin](#admin)

### Request:
`DELETE` /employee/:id/


| param   | description           |
|-------------------|-----------------------|
| `:id`             | `id` from employee  |

### Response Codes:
| code   | description           |
|-------------------|-----------------------|
| 204             | removed with success  |
| 404             | id not found  |
| 400             | id is invalid |

### Example:
```sh
$ curl -v -X DELETE "localhost:8000/employee/1/" -u user:userp123
> DELETE /employee/1/ HTTP/1.1
> Host: localhost:8000
> Authorization: Basic dXNlcjp1c2VycDEyMw==
> User-Agent: curl/7.43.0
> Accept: */*
>
< HTTP/1.0 204 No Content
< Date: Sun, 20 Nov 2016 21:38:39 GMT
< Server: WSGIServer/0.2 CPython/3.5.2
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
<

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


