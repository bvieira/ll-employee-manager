from django.contrib import admin

from employees.models import Employee, Department

admin.site.register(Employee)
admin.site.register(Department)