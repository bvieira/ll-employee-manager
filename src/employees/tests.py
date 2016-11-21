import json
import base64

from django.test import TestCase, Client
from django.contrib.auth.models import User

from employees.models import Employee, Department

class EmployeesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", email="user@user.com", password="1234A5678")
        credentials = base64.b64encode("user:1234A5678".encode()).decode()
        self.client.defaults["HTTP_AUTHORIZATION"] = "Basic %s"%(credentials)


    def test_list_employees(self):
        d = Department.objects.create(name = "department-list")
        Employee.objects.create(name = "user-list", email = "user-list@email.com", department = d)

        response = self.client.get("/employee/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode())
        self.assertTrue(len(content) > 0, "response is empty")
        self.assertContains(response, "user-list@email.com")


    def test_get_employee(self):
        d = Department.objects.create(name = "department-get")
        e = Employee.objects.create(name = "user-get", email = "user-get@email.com", department = d)

        response = self.client.get("/employee/%s/"%(e.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user-get@email.com")

    def test_get_employee_not_found(self):
        response = self.client.get("/employee/9999/")
        self.assertEqual(response.status_code, 404)

    def test_get_employee_invalid_id(self):
        response = self.client.get("/employee/abc/")
        self.assertEqual(response.status_code, 400)


    def test_create_employee(self):
        response = self.client.post("/employee/", json.dumps({"name": "user1", "email": "user1@email.com", "department": "Tecnologia"}), "application/json")
        
        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content.decode())
        self.assertEqual(content["name"], "user1")
        self.assertEqual(content["email"], "user1@email.com")
        self.assertEqual(content["department"], "Tecnologia")

    def test_create_employee_invalid_email(self):
        response = self.client.post("/employee/", json.dumps({"name": "user1", "email": "user1", "department": "Tecnologia"}), "application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_employee_duplicated_email(self):
        d = Department.objects.create(name = "department-duplicated")
        Employee.objects.create(name = "user-duplicated", email = "user-duplicated@email.com", department = d)

        response = self.client.post("/employee/", json.dumps({"name": "user-duplicated2", "email": "user-duplicated@email.com", "department": "department-duplicated"}), "application/json")
        self.assertEqual(response.status_code, 400)


    def test_update_employee(self):
        d = Department.objects.create(name = "department-update")
        e = Employee.objects.create(name = "user-update", email = "user-update@email.com", department = d)

        response = self.client.put("/employee/%s/"%(e.id), json.dumps({"name": "user-update", "email": "user-update1@email.com", "department": "department-update"}), "application/json")
        self.assertEqual(response.status_code, 202)
        content = json.loads(response.content.decode())
        self.assertEqual(content["email"], "user-update1@email.com")

        result = Employee.objects.get(id=e.id)
        self.assertEqual(result.email, "user-update1@email.com")


    def test_update_employee_department(self):
        d = Department.objects.create(name = "department-update")
        e = Employee.objects.create(name = "user-update", email = "user-update@email.com", department = d)

        response = self.client.put("/employee/%s/"%(e.id), json.dumps({"name": "user-update", "email": "user-update@email.com", "department": "department-update1"}), "application/json")
        self.assertEqual(response.status_code, 202)
        content = json.loads(response.content.decode())
        self.assertEqual(content["department"], "department-update1")

        result = Employee.objects.get(id=e.id)
        self.assertEqual(result.department.name, "department-update1")

    def test_update_employee_duplicated_email(self):
        d = Department.objects.create(name = "department-update-duplicated")
        e = Employee.objects.create(name = "user-duplicated", email = "user-duplicated@email.com", department = d)
        Employee.objects.create(name = "user-duplicated1", email = "user-duplicated1@email.com", department = d)

        response = self.client.put("/employee/%s/"%(e.id), json.dumps({"name": "user-duplicated", "email": "user-duplicated1@email.com", "department": "department-update-duplicated"}), "application/json")
        self.assertEqual(response.status_code, 400)

    def test_update_employee_invalid_id(self):
        response = self.client.put("/employee/abc/", json.dumps({"name": "user-duplicated", "email": "user-duplicated1@email.com", "department": "department-update-duplicated"}), "application/json")
        self.assertEqual(response.status_code, 400)


    def test_delete_employee(self):
        d = Department.objects.create(name = "department-delete")
        e = Employee.objects.create(name = "user-delete", email = "user-delete@email.com", department = d)

        response = self.client.delete("/employee/%s/"%(e.id))
        self.assertEqual(response.status_code, 204)
        self.assertRaises(Employee.DoesNotExist, Employee.objects.get, id=e.id)

    def test_delete_employee_not_found(self):
        response = self.client.delete("/employee/9999/")
        self.assertEqual(response.status_code, 404)

    def test_delete_employee_invalid_id(self):
        response = self.client.delete("/employee/abc/")
        self.assertEqual(response.status_code, 400)
