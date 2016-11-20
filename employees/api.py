import base64
from django.contrib.auth import authenticate
from django.forms import ModelForm

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import BadRequest, NotFound

from employees.models import Employee, Department

class EmployeeForm(ModelForm):
    class Meta(object):
        model = Employee
        fields = ['name', 'email']

class DepartmentForm(ModelForm):
    class Meta(object):
        model = Department
        fields = ['name']


class EmployeeResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'email': 'email',
        'department': 'department.name',
    })

    @staticmethod
    def get_department(depName):
        try:
            return Department.objects.get(name = depName)
        except Department.DoesNotExist:
            return Department.objects.create(name = depName)

    def wrap_list_response(self, data):
        return data

    def validate_employee(self, **kwargs):
        dform = DepartmentForm({'name': self.data['department']})
        if not dform.is_valid():
            raise BadRequest(dform.errors)

        if 'instance' in kwargs:
            eform = EmployeeForm(self.data, instance=kwargs['instance'])
        else:
            eform = EmployeeForm(self.data)
        if not eform.is_valid():
            raise BadRequest(eform.errors)
        return (eform.cleaned_data, dform.cleaned_data)

    def is_authenticated(self):
        if self.request_method() == 'GET':
            return True

        if 'HTTP_AUTHORIZATION' in self.request.META:
            auth = self.request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                username, password = base64.b64decode(auth[1]).decode('utf-8').split(':')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    return True
        return False

    def list(self):
        return Employee.objects.all()

    def detail(self, pk):
        if not pk.isdigit():
            raise BadRequest("id:[%s] is invalid" %(pk))
            
        return Employee.objects.get(id=pk)

    def create(self):
        eclean, dclean = self.validate_employee()
        return Employee.objects.create(
            name = eclean['name'],
            email = eclean['email'],
            department = self.get_department(dclean['name'])
        )

    def update(self, pk):
        if not pk.isdigit():
            raise BadRequest("id:[%s] is invalid" %(pk))

        try:
            emp = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            raise NotFound("employee id:[%s] not found" % (pk))

        eclean, dclean = self.validate_employee(instance=emp)

        emp.name = eclean['name']
        emp.email = eclean['email']
        if dclean['name'] != emp.department.name:
            emp.department = self.get_department(dclean['name'])
        emp.save()
        return emp

    def delete(self, pk):
        if not pk.isdigit():
            raise BadRequest("id:[%s] is invalid" %(pk))

        Employee.objects.get(id=pk).delete()
