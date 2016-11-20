from django.conf.urls import url, include
from employees.api import EmployeeResource

urlpatterns = [
    url(r'^', include(EmployeeResource.urls()))
]